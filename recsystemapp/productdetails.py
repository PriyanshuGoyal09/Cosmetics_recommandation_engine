import csv
from jinja2 import Template

def add_data_to_template(csv_file, template_file, output_file):
   
    # Read the CSV file
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    # Load the template
    with open(template_file, 'r') as template_file:
        template = Template(template_file.read())

    # Render the template with the data
    output = template.render(data=data)

    # Write the output to a file
    with open(output_file, 'w') as outfile:
        outfile.write(output)

# Example usage:
csv_file = 'E:\projects\Cosmetics_recommandation_engine\cosmetics.csv'
template_file = 'E:\projects\Cosmetics_recommandation_engine\recsystemapp\templates\product_detail_template.html'
output_file = 'output.html'
add_data_to_template(csv_file, template_file, output_file)