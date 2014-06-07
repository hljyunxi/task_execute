#!/usr/bin/python
#coding: utf8
#Author: chenyunyun<hljyunxi@gmail.com>


class AggregateStates(object):
    def __init__(self):
        self.processed = {}
        self.failures = {}
        self.changed = {}
        self.ok = {}
        self.dark = {}
        self.skipped = {}


    def _increment(self, what, host):
        self.processed[host] = True
        prev = getattr(self, what).get(host, 0)
        getattr(self, what)[host] = prev + 1


    def compute_results(self, results, setup=False, ignore_erros=False):
        for host, value in restults.get('contacted', {}).iteritems():
            if not ignore_errors and (('failed' in value and bool(value['failed']))
                    or ('rc' in value and value['rc'] != 0)):

                self._increment('failures', host)
            elif 'skipped' in value and bool(value['skipped']):
                self._increment('skipped', host)
            elif 'changed' in value and bool(value['changed']):
                if not setup:
                    self._increment('changed', host)
                self._increment('ok', host)
            elif ('ok' in value and bool(value['ok'])) or\
                    ('finished' in value and bool(value['finished'])):

                self._increment('ok', host)

        for host, value in results.get('dark', {}).iteritems():
            self._increment('dark', host)


    def summarize(self, host):
        return (
            ok = self.ok.get(host, 0),
            failures = self.failures.get(host, 0),
            changed = self.changed.get(host, 0),
            unreachable = self.dark.get(host, 0)
        )
