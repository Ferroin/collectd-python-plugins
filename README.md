# collectd-python-plugins #
This is a collection of various collectd plugins I've written in Python.
They cover a handful of things that I care about tracking but I'm to
lazy to get proper plugins into the collectd distribution for.

All of them require the 'python' plugin for collectd, and require that's
it's built using at least Python 3.4.

Setup is pretty simple, add the included types.db file to your
collectd.conf, then add entries for each of the plugins you want to load.

Unless otherwise noted, all the plugins here are licensed under a 3-clause
BSD license.

### Included Plugins ###
###### linux\_interrupts.py ######
This puls some stats out of /proc/interrupts on Linux systems.  Unlike the
'irq' plugin for collectd, this tracks abstract interrupt rates instead
of tracking physical interrupts.  In particular, it reports rates for
the following interrupt types:
* Non-maskable interrupts
* Local timer interrupts
* Spurrious interrupts: Normally this should be zero, if it isn't,
  you've got a problem with your hardware, your firmware, or your drivers.
* Performance monitoring interrupts
* Rescheduling interrupts
* Function call interrupts
* TLB Shootdown interrupts: Higher values here correlate to lower performance.
* Thermal event interrupts: Seeing anything but zero here means your
  machine is having thermal management issues.
* Threshold APIC interrupts
* MCE interrupts: Similar to the thermal and spurrious interrupts,
  anything but zero here means something's wrong with your system.
* Machine check poll interrupts

Metrics are reported with a plugin name of `interrupts` and type of
`linux_interrupts`.

This plugin requires a working /proc filesystem with /proc/interrupts
readable by whatever user you run collectd as.

There are no configuration options.

###### linux\_softirqs.py ######
While linux\_interrupts tracks ISR execution for specific types of
interrupt, linux\_softirqs tracks execution of deferred ISR's, also
known as softirqs or tasklets.  There are a total of 10 softirqs we
recognize:
* hi: High priority tasklets.
* timer: Kernel timers.
* net\_tx: Network transmission tasklets.
* net\_rx: Network reciever tasklets.
* block: Various block-layer tasklets (mostly of interest to people
  using SCSI storage devices).
* irq\_pool: Tasklet for the `irqpoll` kernel parameter (should usually
  be 0 unless you're using the aforementioned kernel parameter).
* tasklet: Generic priority tasklets.
* sched: Scheduler tasklets.
* hrtimer: Software high-resolution timer tasklets.
* rcu: Tasklets for handling RCU updates.

Which of these have practicla meaning depends on your system.

Metrics are reported with a plugin name of `softirqs` and a type of
`linux_softirqs`.

This plugin requires a working /proc filesystem with /proc/softirqs
readable by whatever user you run collectd as.

There are no configuration options.
