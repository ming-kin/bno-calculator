from flask import Flask, request, render_template
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Render the form
    return render_template('index.html')

@app.route('/check_dates', methods=['POST'])
def check_dates():
    # Get the start and end dates from the form
    start = datetime.strptime(request.form.get('start'), '%Y-%m-%d')
    end = datetime.strptime(request.form.get('end'), '%Y-%m-%d')

    # Get the absence periods from the form
    absence_from = request.form.getlist('absence_from[]')
    absence_to = request.form.getlist('absence_to[]')

    # Create a list of absence periods
    absences = [{'from': datetime.strptime(from_date, '%Y-%m-%d'), 'to': datetime.strptime(to_date, '%Y-%m-%d')} 
                for from_date, to_date in zip(absence_from, absence_to)]
    
    # Call function to calculate absences
    absences_per_year, exceeds_limit = calculate_absences(absences, start, end)

    # Pass the results to the template
    return render_template('results.html', absences=absences_per_year, exceeds_limit=exceeds_limit)

def calculate_absences(absences, start, end):
    # Initialize an empty dictionary to hold the results
    results = {}
    exceeds_limit = False

    # Define the start and end dates of the first 12-month period
    period_start = start
    period_end = start + timedelta(days=365)  # This will be 365 days after the start date

    # Initialize a counter for the number of 12-month periods
    period_counter = 1

    # Loop through each 12-month period
    while period_start < end:
        # Initialize a counter for the number of absences
        absences_count = 0

        # Loop through each absence
        for absence in absences:
            # Check if the absence falls within the 12-month period
            if max(absence['from'], period_start) <= min(absence['to'], period_end):
                # Add the number of absence days to the counter
                absences_count += (min(absence['to'], period_end) - max(absence['from'], period_start)).days + 1

        # Check if absences_count exceeds 180
        if absences_count > 180:
            exceeds_limit = True

        # Add the total number of absences for the 12-month period to the results
        results[f"Period {period_counter} ({period_start.strftime('%Y-%m-%d')} - {period_end.strftime('%Y-%m-%d')})"] = absences_count

        # Move to the next 12-month period
        period_start = period_start + timedelta(days=365)
        period_end = period_end + timedelta(days=365)
        period_counter += 1

    return results, exceeds_limit

if __name__ == '__main__':
    app.run(debug=True)