# Kiwi.com _Python víkend_ task
If you have applied for our Python _vikend course_ this task serves to asess if you have sufficient knowledge to enjoy and learn something on our course.

## Task
Your task is to use our _flights_ API to find a flight and book the flight on the _booking_ API. If it sounds too complicated. Don't worry, it's not.

## APIs
### Flights
We at _Kiwi.com_ use simple APIs based on HTTP, usually with payload in JSON format. If you've never used an API click here:

https://api.skypicker.com/flights?v=3&daysInDestinationFrom=6&daysInDestinationTo=7&flyFrom=49.2-16.61-250km&to=dublin_ie&dateFrom=03/09/2017&dateTo=09/09/2017&typeFlight=return&adults=1&limit=60

Now you have.
Our API for searching flights is public, so you can find the documentation in Apiary http://docs.skypickerpublicapi.apiary.io/#reference/flights
### Booking
Now, that was easy. The world is not perfect and not everything is documented so there is no documentation provided for this API. To book the flight, you'll need to use the booking API (which has been created solely for the purpose of the task and no payment is required).

The endpoint is here:
http://37.139.6.125:8080/booking

You'll just have to figure out how it works and book the flight. Good luck!

## Requirements
* The solution must be written in Python 3 (or 2 if you must)
* The following invocations of your program must work
    * `./book_flight.py --date 2017-10-13 --from BCN --to DUB --one-way`
    * `./book_flight.py --date 2017-10-13 --from LHR --to DXB --return 5`
    * `./book_flight.py --date 2017-10-13 --from NRT --to SYD --cheapest`
    * `./book_flight.py --date 2017-10-13 --from CPH --to MIA --shortest`

    where `--one-way` (make this the default option) indicates need of flight only to location and `--return 5` should book flight with passenger staying 5 nights in destination,
    
    `--cheapest` (default) will book the cheapest flight and `--shortest` will work similarly
    
    The program will output a [PNR number](https://en.wikipedia.org/wiki/Passenger_name_record) which serves as confirmation of booking

    The `--from` and `--to` parameters only need to support [airport IATA codes](https://en.wikipedia.org/wiki/International_Air_Transport_Association_airport_code)
    
## Submitting
Please send your coded solutions to pythonvikend@kiwi.com , most preferably posted online on places like GitHub or elsewhere, but attachment files are also OK, I guess, if you don't wish to publish it.

