'''
Copyright (c) 2017, Austin S. Hemmelgarn
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of Austin S. Hemmelgarn nor the names of any other
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''
import collectd
import time

# Define the order we submit metrics in.
_softirqs_order = [
    'hi',
    'timer',
    'net_tx',
    'net_rx',
    'block',
    'irq_poll',
    'tasklet',
    'sched',
    'hrtimer',
    'rcu'
]

def intitersum(data):
    '''Sum up the numeric items in data.

       This takes an iterable and returns the sum of every item in it
       that can be converted to an int.'''
    total = 0
    for item in data:
        try:
            total = total + int(item)
        except:
            pass
    return total

def _get_softirqs():
    '''Extract data from /proc/softirqs.

       Returns a tuple of (timestamp, values), where timestamp is the
       UNIX time the data was collected, and values is a dict of the
       data collected, with keys matching the sub-types in the
       linux_softirqs type.'''
    results = dict()
    with open('/proc/softirqs', 'r') as proc:
        tstamp = time.time()
        data = proc.read()
    for line in data.splitlines():
        line = line.split()
        if line[0].lower() == 'cpu0':
            continue
        counter = line[0].rstrip(':').lower()
        results[counter] = intitersum(line[1:])
    return (tstamp, results)

def read():
    '''Read our metrics and report them to collectd.'''
    data = _get_softirqs()
    dataset = collectd.Values()
    dataset.host = ''
    dataset.plugin = 'softirqs'
    dataset.plugin_instance = ''
    dataset.time = data[0]
    dataset.type = 'linux_softirqs'
    dataset.type_instance = ''
    dataset.values = []
    for index in _softirqs_order:
        if index in data[1].keys():
            dataset.values.append(data[1][index])
        else:
            dataset.values.append(0)
    dataset.dispatch()
    return True

def config(conf):
    '''Initial configuration.'''
    return True

def init():
    '''Actual setup.'''
    collectd.register_read(read)
    return True

def shutdown():
    '''Final teardown.'''
    return True

collectd.register_config(config)
collectd.register_init(init)
collectd.register_shutdown(shutdown)
