#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import click
import datetime
import json
import requests
       
    
@click.command()
@click.option('--date', '_date', type=str, prompt='Insert departure date')
@click.option('--from', 'flyFrom', type=str, prompt='Insert departure destination')
@click.option('--to', 'to', type=str, prompt='Insert arrival destination')
@click.option('--cheapest', 'sort', flag_value='price', default='price')
@click.option('--shortest', 'sort', flag_value='duration')
@click.option('--one-way', 'nights_in_destination', flag_value=0, type=int, default=0)
@click.option('--return', 'nights_in_destination', type=int)
def main(_date, flyFrom, to, sort, nights_in_destination):
    
    # try to get date from input string
    try:
        departureDate = datetime.datetime.strptime(_date, "%Y-%m-%d").date().strftime('%d/%m/%Y')
    except:
        print('Try --date in YYYY-MM-DD format')
        return 1
            
    # fill query string 
    querystring = {
        'v': 3, # use version 3, as in example
        'flyFrom': flyFrom,
        'to': to, 
        'dateFrom': departureDate,
        'dateTo': departureDate,
        'typeFlight': 'return' if nights_in_destination  else 'oneway', # 'return' instead of 'round', as in example
        'daysInDestinationFrom': int(nights_in_destination) if nights_in_destination is not None else 0,
        'daysInDestinationTo': int(nights_in_destination) if nights_in_destination is not None else 0,
        'sort': sort,
        'limit':1
    }
    flights_url = "https://api.skypicker.com/flights" 
    response = requests.get(flights_url, params=querystring) # execute request, may be in try-except
    flights_data = response.json() # extract data from json
        
    try:
        top_flight = flights_data['data'][0] # get best result
    except:
        click.echo('404 Flight not Found!')
        return 1
    dTimeUTC = datetime.datetime.utcfromtimestamp(top_flight['dTimeUTC']) # get datetime from timestamp
    aTimeUTC = datetime.datetime.utcfromtimestamp(top_flight['aTimeUTC']) # ^^^
    
    # clear screen, print header
    # output is formated to 80 chars per line
    click.clear()
    click.echo('#' * 80)
    click.echo('#{:^78}#'.format(' '))
    click.echo('# {:^76} #'.format('We choose for you this flight:'))
    click.echo('#{:^78}#'.format(' '))
    click.echo('#' * 80)
    
    # print basic info
    click.echo('Departure time [UTC]:{:>59}'.format(str(dTimeUTC)))
    click.echo('Arrival time [UTC]:{:>61}'.format(str(aTimeUTC)))
    click.echo('Price:{:>70} {:>3}'.format(top_flight['price'], flights_data['currency']))
    click.echo('Fly duration:{:>67}'.format(top_flight['fly_duration']))
    
    # print flight route foreach
    for single_flight in top_flight['route']:
        dTimeUTC = datetime.datetime.utcfromtimestamp(single_flight['dTimeUTC'])
        aTimeUTC = datetime.datetime.utcfromtimestamp(single_flight['aTimeUTC'])
        
        click.echo('\n{:^80}'.format('{cityFrom} {flyTo} > {cityTo} {flyFrom}'.format(** single_flight)))
        click.echo('   Departure time [UTC]:{:>53}   '.format(str(dTimeUTC)))
        click.echo('   Arrival time [UTC]:{:>55}   '.format(str(aTimeUTC)))
    
    # ask for continue
    click.confirm('\nDo you want book this flight?', abort=True)
    
    # input data for booking
    title = click.prompt('Please choose title [Mr/Mrs]', type=click.Choice(['Mr', 'Mrs']))
    firstName = click.prompt('Please enter your first name', type=str)
    lastName = click.prompt('Please enter your last name', type=str)
    email = click.prompt('Please enter your email', type=str)
    click.echo('Please enter your birthday')
    birthday = {}
    birthday['y'] = click.prompt('\tyear [1900-{}]'.format(datetime.datetime.now().year), type=int)
    birthday['m'] = click.prompt('\tmonth [1-12]', type=int)
    birthday['d'] = click.prompt('\tday [1-31]', type=int)
    documentID = click.prompt('Please enter your documentID', type=str)
    
    booking_url = "http://37.139.6.125:8080/booking"
    headers = {
        'content-type': "application/json", # set header to JSON
    }
    # fill data for booking request
    data = {
        "currency": flights_data['currency'],
        "booking_token": top_flight['booking_token'],
        "passengers": [
            {
                "birthday": "{y}-{m}-{d}".format( ** birthday),
                "documentID": documentID,
                "lastName": lastName,
                "firstName": firstName,
                "title": title,
                "email": email
            }
        ]
    }
    # execute booking request
    response = requests.post(booking_url, data=json.dumps(data), headers=headers)

    try:
        booking_data = response.json()
        click.echo('\n>> Your PNR number is: {}\n'.format(str(booking_data['pnr'])))
    except:
        click.echo(response.text)
        return 1
    return 0

if __name__ == '__main__':
    main()