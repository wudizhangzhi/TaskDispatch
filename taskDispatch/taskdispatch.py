import json

__all__ = ['TaskDispatch']


def _s(i):
    if isinstance(i, bytes):
        return i.decode('utf8')
    return i


class TaskDispatch(object):
    """任务调度中心"""

    START = 'start'
    PAUSE = 'pause'
    TASK_STATUS_CHOICES = (
        START, PAUSE
    )

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _queue_task_key(queue, task_id):
        return '%s_%s' % (queue, task_id)

    @staticmethod
    def _queue_hash_key(queue):
        return 'QUEUE_HASH_%s' % queue

    @staticmethod
    def _f(t):
        return json.dumps(t)

    def _push_task(self, queue, task_id, task):
        """保存任务到任务id队列"""
        return self.client.lpush(self._queue_task_key(queue, task_id), self._f(task))

    def _pop_task(self, queue, task_id):
        """从任务id队列取出任务"""
        ret = self.client.rpop(self._queue_task_key(queue, task_id))
        try:
            return json.loads(ret)
        except:
            return ret

    def _save_task_id(self, queue, task_id):
        return self.client.hset(self._queue_hash_key(queue), task_id, self.START)

    def _hgetall_task_id(self, queue):
        """获取队列中所有的任务id"""
        return self.client.hgetall(self._queue_hash_key(queue))

    def _hdel_task_id(self, queue, task_id):
        """删除队列中的任务id"""
        return self.client.hdel(self._queue_hash_key(queue), task_id)

    def task_len(self, queue, task_id):
        """
        任务剩余长度
        :param queue:
        :param task_id:
        :return:
        """
        return self.client.llen(self._queue_task_key(queue, task_id))

    def is_task_end(self, queue, task_id):
        """任务队列是否完成"""
        return self.task_len(queue, task_id) == 0

    def pause_task(self, queue, task_id):
        """暂停任务"""
        return self.client.hset(self._queue_hash_key(queue), task_id, self.PAUSE)

    def stop_task(self, queue, task_id):
        """停止任务"""
        self.client.hdel(self._queue_hash_key(queue), task_id)
        return self.client.delete(self._queue_task_key(queue, task_id))

    def push(self, queue, task_id, task):
        """
        任务队列添加任务
        :param queue: 队列
        :param task_id: 任务唯一标识
        :param task: 任务
        :return:
        """
        # 保存task_id
        self._save_task_id(queue, task_id)
        # 插入task queue
        self._push_task(queue, task_id, task)

    def pop(self, queue):
        """
        任务队列取出任务
        :param queue: 任务队列
        :return:
        """
        # 查询任务对应的任务id
        queue_task_id_dict = self._hgetall_task_id(queue)
        # TODO 一些调度, 优先级
        from random import choice
        handled_queue = [k for k, v in queue_task_id_dict.items() if _s(v) != self.PAUSE]
        task_id_choice = choice(handled_queue) if handled_queue else None
        # 从对应的任务id队列取出任务
        if not task_id_choice:
            return None, None
        task_id_choice = _s(task_id_choice)
        ret = self._pop_task(queue, task_id_choice)
        # 任务id队列如果空了。删除
        if self.is_task_end(queue, task_id_choice):
            self._hdel_task_id(queue, task_id_choice)
        return task_id_choice, ret
