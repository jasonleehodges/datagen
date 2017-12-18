<h1>DataGen</h1>
<p>A simple wrapper for the faker and random python modules that will quickly generate fake data in 5 parallel threads 
and export to a csv. Instantiate the class with a string filename as well as the number of rows you wish to generate
as arguments to the constructor method. The file will be stored in the same directory that the python script is executed from.
</p>
<p>
Data can be generated with or without a date column. Call the dates method with a start date string and an end date string
(in the YYYY-MM-DD format) in order to set the date column to generate random dates between the start and end date.
</p>
<strong>Known limitations:</strong>
<ul>
<li>Requires Python 3, the multiprocess module, and the typing module for type hints.</li>
<li>Number of rows should be a multiple of 10 in order to split up the work between threads equally.</li>
</ul>

<h3>
Example:
</h3>
<pre>
dg = DataGen("fakedata_1000",1000)
dg.dates("2017-01-01","2017-12-31")
dg.generate()
</pre>
