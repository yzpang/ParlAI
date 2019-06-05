#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""
Provides utilities for logging metrics.

This file provides interface to log metrics in tensorboard or visdom.

If you use visdom logging, instructions please follow the instructions
at https://github.com/facebookresearch/visdom to install visdom,
and launch a local visdom server.

.. code-block: none

    visdom  # i.e., in screen or tmux

If you use tensorboard logging, all event folders will be stored in
``PARLAI_DATA/tensorboard`` folder. In order to Open it with TB, launch
tensorboard as:

.. code-block: none

   tensorboard --logdir <PARLAI_DATA/tensorboard> --port 8888.
"""

# TODO: update this with pytorch 1.1's tensorboard API

import os


class Logger(object):
    """Main class for logging API."""

    @staticmethod
    def add_cmdline_args(argparser):
        logger = argparser.add_argument_group('Logging Arguments')
        logger.add_argument('-logmet', '--logger-metrics', type=str, default=None,
            help='Specify metrics which you want to track. These will be extracted '
                 'from the report dictionary.',
            hidden=True)
        return logger
    
    def add_metrics(self, setting, step, report):
        """
        Add all metrics from tensorboard_metrics opt key.

        :param setting: graph titles, whether doing training or evaluation
        :param step: graph x axis, typically number of parleys in training or wall
            clock time in validation
        :param report: dictionary containing metric keys and values
        """
        raise RuntimeError('Subclass must implement this.')


class VisdomLogger(Logger):
    """Log objects to Visdom."""

    @staticmethod
    def add_cmdline_args(argparser):
        logger = argparser.add_argument_group('Visdom Arguments')
        super(Logger, cls).add_cmdline_args(argparser)
        return logger

    def __init__(self, opt, shared=None):
        try:
            import visdom
        except ImportError:
            raise ImportError('Need to install Visdom: go to github.com/facebookresearch/visdom')
        
        self.vis = visdom.Visdom()
        self.metrics = {}
        for metric in opt.get('logger_metrics'):
            self.metrics[metric] = []

    def add_metrics(self, setting, step, report):
        """
        Add all metrics from tensorboard_metrics opt key.

        :param setting: graph titles, whether doing training or evaluation
        :param step: graph x axis, typically number of parleys in training or wall
            clock time in validation
        :param report: dictionary containing metric keys and values
        """
        for key, queue in self.metrics.items():
            if key in report:
                queue.append((step, report[key]))
    
    



class TensorboardLogger(Logger):
    """Log objects to tensorboard."""

    _shared_state = {}

    @staticmethod
    def add_cmdline_args(argparser):
        """Add tensorboard CLI args."""
        logger = argparser.add_argument_group('Tensorboard Arguments')
        logger.add_argument(
            '-tblog', '--tensorboard-log', type='bool', default=False,
            help="Tensorboard logging of metrics, default is %(default)s",
            hidden=True
        )
        logger.add_argument(
            '-tbtag', '--tensorboard-tag', type=str, default=None,
            help='Specify all opt keys which you want to be presented in in TB name',
            hidden=True
        )
        logger.add_argument(
            '-tbmetrics', '--tensorboard-metrics', type=str, default=None,
            help='Specify metrics which you want to track, it will be extracted '
                 'from report dict.',
            hidden=True
        )
        logger.add_argument(
            '-tbcomment', '--tensorboard-comment', type=str, default='',
            hidden=True,
            help='Add any line here to distinguish your TB event file, optional'
        )
        super(Logger, cls).add_cmdline_args(argparser)
        return logger

    def __init__(self, opt):
        self.__dict__ = self._shared_state
        try:
            from tensorboardX import SummaryWriter
        except ImportError:
            raise ImportError(
                'Please `pip install tensorboardX` for logs with TB.')

        if opt['tensorboard_tag'] is None:
            tensorboard_tag = opt['starttime']
        else:
            tensorboard_tag = opt['starttime'] + '__'.join([
                i + '-' + str(opt[i])
                for i in opt['tensorboard_tag'].split(',')
            ])
        if opt['tensorboard_comment']:
            tensorboard_tag += '__' + opt['tensorboard_comment']

        tbpath = os.path.join(os.path.dirname(opt['model_file']), 'tensorboard')
        print('[ Saving tensorboard logs here: {} ]'.format(tbpath))
        if not os.path.exists(tbpath):
            os.makedirs(tbpath)
        self.writer = SummaryWriter(
            log_dir='{}/{}'.format(tbpath, tensorboard_tag))
        if opt['tensorboard_metrics'] is None:
            self.tbmetrics = ['ppl', 'loss']
        else:
            self.tbmetrics = opt['tensorboard_metrics'].split(',')

    def add_metrics(self, setting, step, report):
        """
        Add all metrics from tensorboard_metrics opt key.

        :param setting: whatever setting is used, train valid or test, it will
            be just the title of the graph
        :param step: num of parleys (x axis in graph), in train - parleys, in
            valid - wall time
        :param report: from TrainingLoop
        """
        for met in self.tbmetrics:
            if met in report.keys():
                self.writer.add_scalar(
                    "{}/{}".format(setting, met),
                    report[met],
                    global_step=step
                )

    def add_scalar(self, name, y, step=None):
        """
        Add a scalar.

        :param str name:
            the title of the graph, use / to group like "train/loss/ce" or so
        :param y:
            value
        :param step:
            x axis step
        """
        self.writer.add_scalar(name, y, step)

    def add_histogram(self, name, vector, step=None):
        """Add a histogram."""
        self.writer.add_histogram(name, vector, step)

    def add_text(self, name, text, step=None):
        """Add text."""
        self.writer.add_text(name, text, step)
