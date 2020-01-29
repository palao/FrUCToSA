########################
Architecture of FrUCToSA
########################


************
Introduction
************

``FrUCToSA`` has several components, as described in the ``README``:

1. ``fructosad`` itself is the main program from the point of view of the end user.
   It controls all the other components. It runs in the background.
2. ``LiMon`` (**Li**\ ght **Mon**\ intor): this component is in charge of collecting
   data and send it to the given destinations. ``LiMon`` is divided into two programs:

   * ``lagent``: that collects raw data from the monitored systems and sends it to the
     specified location(s).
   * ``lmaster``: which controls the ``lagent``\ s (start, stop and configure agents).

3. ``PerA``: **Per**\ formance **A**\ nalyzer. It analyzes the raw data obtained by
   ``LiMon``, *cooks* it if necessary, and classifies the data.

   
``fructosad``
=============

