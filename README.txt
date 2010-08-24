Introduction
============

This package is a plugin for the `ftw.publisher` products. It adds a 
confguration option to the `ftw.publisher` control panel.

The package sends - when enabled - in a defined interval (e.g. each
day) a statistics e-mail to the defined e-mail addresses.
It`s attached to the `IQueueExecutedEvent` event of the
`ftw.publisher.sender`, so no additional cronjob / ClockServer is
required.
