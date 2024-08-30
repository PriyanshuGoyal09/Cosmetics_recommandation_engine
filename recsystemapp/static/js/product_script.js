import Papa from 'papaparse';
import Handlebars from 'handlebars';

// Function to read CSV file and populate template
function populateTemplate(csvFile) {
    // Read CSV file
    Papa.parse(csvFile, {
      header: true,
      complete: function(results) {
        // Get the first row of data (assuming it's the product data)
        const productData = results.data[0];
  
        // Load the product detail template
        fetch('product-detail-template.html')
          .then(response => response.text())
          .then(template => {
            // Create a template engine instance
            const templateEngine = Handlebars.create();
  
            // Compile the template
            const compiledTemplate = templateEngine.compile(template);
  
            // Render the template with the product data
            const html = compiledTemplate(productData);
  
            // Append the rendered HTML to the page
            document.getElementById('product-detail-container').innerHTML = html;
          });
      }
    });
  }
  
  // Example usage:
  const csvFile = 'cosmetics.csv';
  populateTemplate(csvFile);