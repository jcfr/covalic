#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from collections import defaultdict


class MetricScore(object):
    """
    For each metric being scored, call the score method of this class. It will
    call into the per-metric scoring implementation, which is passed both the
    average score as well as all of the individual dataset scores.
    """
    @classmethod
    def score(cls, metric):
        """
        Compute the score value for the given metric. A higher score is better.
        """
        fn = metric['metric'].replace(' ', '').lower()

        if not hasattr(cls, fn):
            raise Exception('Invalid metric: {} ({}).'.format(
                            metric['metric'], fn))

        return getattr(cls, fn)(metric['_avg'], metric['datasets'])

    @staticmethod
    def dice1(avg, datasets):
        return avg

    @staticmethod
    def dice2(avg, datasets):
        return avg

    @staticmethod
    def adb1(avg, datasets):
        return avg

    @staticmethod
    def adb2(avg, datasets):
        return avg

    @staticmethod
    def hdb1(avg, datasets):
        return avg

    @staticmethod
    def hdb2(avg, datasets):
        return avg

    @staticmethod
    def sens1(avg, datasets):
        return avg

    @staticmethod
    def sens2(avg, datasets):
        return avg

    @staticmethod
    def spec1(avg, datasets):
        return avg

    @staticmethod
    def spec2(avg, datasets):
        return avg


def computeAverageScores(score):
    """
    Compute the average score for each metric and add it to the score list
    under the name "Average".

    :param score: The score object to compute the average of. The result of the
        computation is placed at the head of the list.
    :type score: list
    """
    sums = defaultdict(float)

    for dataset in score:
        for metric in dataset['metrics']:
            sums[metric['name']] += float(metric['value'])

    n = float(len(score))
    metrics = [{'name': k, 'value': s / n} for k, s in sums.iteritems()]

    score.insert(0, {
        'dataset': 'Average',
        'metrics': metrics
    })


def computeOverallScore(score):
    """
    Compute the overall score based on the matrix of individual scores. The
    computed value will be used to define the total ordering of submissions
    to a given phase.

    :param score: The score object (metric-major, dataset-minor grouping)
    :type score: dict
    """
    return 123
    #return reduce(lambda x, y: x + MetricScore.score(y), score, 0)
