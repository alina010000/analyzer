import pandas as pd
import os
from collections import Counter
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Define global variables
attribute = None
column_x = None
column_y = None
op = None
rows = None
columns = None
data = None
missing_values = None


def index(request):
    return render(request, 'analyzer/index.html')


def features(request):
    return render(request, 'analyzer/features.html')


def upload(request):
    context = {}

    global attribute, column_x, column_y, op

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        op = request.POST.get('operation')

        if op == 'solo':
            attribute = request.POST.get('attributeid')
        else:
            column_x = request.POST.get('column_x')
            column_y = request.POST.get('column_y')

        # Check if the uploaded file is a CSV
        if uploaded_file.name.endswith('.csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            file_directory = os.path.join(os.getcwd(), 'media', name)
            readfile(file_directory)

            request.session['attribute'] = attribute

            if data is None:
                messages.warning(request, 'Error reading CSV file. Please check the file format.')
            elif op == 'solo' and attribute not in data.columns:
                messages.warning(request, 'Please write the column name correctly')
            else:
                return redirect('analyzer:graph')
        else:
            messages.warning(request, 'File was not uploaded. Please use .csv file extension!')

    return render(request, 'analyzer/upload.html', context)


def readfile(filename):
    global rows, columns, data, missing_values

    # Attempt to read the CSV file with default settings
    try:
        data = pd.read_csv(filename)
    except pd.errors.ParserError:
        # If default settings fail, attempt to read with different settings
        try:
            data = pd.read_csv(filename, delimiter=';')  # Example: Using ';' as delimiter
        except pd.errors.ParserError:
            # Handle other parsing errors if necessary
            data = None

    if data is not None:
        rows, columns = data.shape

        # Find missing values
        missing_values = data.isnull().sum().sum()


def graph(request):
    global attribute, column_x, column_y, op, data

    if data is None:
        messages.warning(request, 'Error reading CSV file. Please check the file format.')
        return redirect('analyzer:upload-data')

    # Display summary message
    message = f'Detail:  {rows} rows and {columns} columns. Missing data: {missing_values}'
    messages.warning(request, message)

    if op == 'solo':
        if attribute not in data.columns:
            messages.warning(request, 'Please write the column name correctly')
            return redirect('analyzer:upload-data')

        # Solo visualization
        dashboard = list(data[attribute])
        my_dashboard = dict(Counter(dashboard))

        listkeys = list(my_dashboard.keys())
        listvalues = list(my_dashboard.values())

        context = {
            'listkeys': listkeys,
            'listvalues': listvalues,
            'op': op,
        }
    else:
        # Relation visualization
        if column_x not in data.columns or column_y not in data.columns:
            messages.warning(request, 'Please write the column names correctly')
            return redirect('analyzer:upload-data')

        x_values = list(data[column_x])
        y_values = list(data[column_y])

        context = {
            'x_values': x_values,
            'y_values': y_values,
            'op': op,
            'column_x': column_x,
            'column_y': column_y,
        }

    return render(request, 'analyzer/graph.html', context)
