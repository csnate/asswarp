ASSWARP
=======

Automatic Scoring System With A Raspberry Pi

We connected 2 vibration sensors to the underside of the goals of a Tornado foosball table, sent the signals with pull down resistors (1 M) to a MCP3002 Analog to Digital Converter (ADC), then sent those signals to the SPI interface of a Raspberry Pi.  The code to read signals from the ADC for the Raspberry Pi is contained in the "controller" folder. 

When a goal is scored, a request is made to a Node JS server, which then displays the current teams' score using Jade.  The code for the Node server and the Jade template is in the "node" fodler.

High Level Overview
--------------
![](https://raw.githubusercontent.com/csnate/asswarp/master/images/HighLevel.png)


Vibation Sensors to ADC to RPi connections
-------------------
![](https://raw.githubusercontent.com/csnate/asswarp/master/images/ADC2RPi.png)

This image (taken from [Reading from a MCP3002 analog-to-digital converter](http://raspberry.io/projects/view/reading-from-a-mcp3002-analog-to-digital-converter/)) comes close to our setup.  We made the following connections:

<table>
	<thead>
		<tr>
			<th style="background-color:#aaa">ADC</th>
			<th style="background-color:#aaa">RPi</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td style="background-color:#eee">CS</td>
			<td style="background-color:#eee">SP10 CE0 N (24)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">CH0</td>
			<td style="background-color:#eee">Vibration Sensor 1 (Black Team)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">CH1</td>
			<td style="background-color:#eee">Vibration Sensor 2 (Yellow Team)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">VSS</td>
			<td style="background-color:#eee">GND (6)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">VDD</td>
			<td style="background-color:#eee">3v3 (1)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">CLK</td>
			<td style="background-color:#eee">SP10 SCLK (23)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">DOUT</td>
			<td style="background-color:#eee">SP10 MISO (21)</td>
		</tr>
		<tr>
			<td style="background-color:#eee">DIN</td>
			<td style="background-color:#eee">SP10 MOSI (19)</td>
		</tr>
	</tbody>
</table>
