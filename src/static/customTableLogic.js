function generateTable() {
    const rows = document.getElementById('rows').value;
    const cols = document.getElementById('cols').value;

    document.getElementById('numberInputTable').innerHTML = '';

    const table = document.getElementById('numberInputTable');
    for (let i = 0; i < rows; i++) {
        const row = table.insertRow();
        for (let j = 0; j < cols; j++) {
            const cell = row.insertCell();
            const input = document.createElement('input');
            input.type = 'number';
            cell.appendChild(input);
        }
    }
}


function addRow() {
  const table = document.getElementById('colorNameTable').getElementsByTagName('tbody')[0];
  const rows = table.getElementsByTagName('tr');
  const newIndex = rows.length + 1; // Calculate new index based on current rows

  // Create a new row
  const newRow = document.createElement('tr');

  // Add index cell (no input, just a number)
  const numberCell = document.createElement('td');
  numberCell.innerText = newIndex; // Set the index text

  // Add color cell
  const colorCell = document.createElement('td');
  colorCell.innerHTML = '<input type="color" />';

  // Add name cell
  const nameCell = document.createElement('td');
  nameCell.innerHTML = '<input type="text" placeholder="Enter name" />';

  // Append cells to the new row
  newRow.appendChild(numberCell);
  newRow.appendChild(colorCell);
  newRow.appendChild(nameCell);

  // Append the new row to the table body
  table.appendChild(newRow);

  // Re-index rows (optional safeguard)
  updateIndexes();
}

function removeRow() {
  const table = document.getElementById('colorNameTable').getElementsByTagName('tbody')[0];
  const rows = table.getElementsByTagName('tr');

  // Only remove if there are rows left
  if (rows.length > 0) {
      table.deleteRow(rows.length - 1); // Remove the last row
      updateIndexes(); // Update indexes after removal
  }
}

function updateIndexes() {
  const table = document.getElementById('colorNameTable').getElementsByTagName('tbody')[0];
  const rows = table.getElementsByTagName('tr');

  // Loop through rows and update index column
  for (let i = 0; i < rows.length; i++) {
      const indexCell = rows[i].getElementsByTagName('td')[0];
      indexCell.innerText = i + 1; // Update index (1-based)
  }
}



function sendTableData() {
  // Extract data from "numberInputTable"
  const numberInputTable = document.getElementById("numberInputTable");
  const numberRows = numberInputTable.rows;
  const tableData = [];

  for (let i = 0; i < numberRows.length; i++) {
      const cells = numberRows[i].cells;
      const rowData = [];
      for (let j = 0; j < cells.length; j++) {
          const cell = cells[j];
          // Check if the cell contains an input element
          const input = cell.querySelector('input');
          if (input) {
              rowData.push(input.value); // Get value from the input element
          } else {
              rowData.push(cell.innerText.trim()); // Get the text content
          }
      }
      tableData.push(rowData); // Add row to tableData
  }

  // Extract colors and names from "colorNameTable"
  const colorNameTable = document.getElementById("colorNameTable");
  const colorRows = colorNameTable.getElementsByTagName("tbody")[0].rows;
  const colors = [];
  const names = [];

  for (let i = 0; i < colorRows.length; i++) {
      const colorInput = colorRows[i].cells[1].querySelector("input[type='color']");
      const nameInput = colorRows[i].cells[2].querySelector("input[type='text']");
      if (colorInput) {
          colors.push(colorInput.value); // Extract color value
      }
      if (nameInput) {
          names.push(nameInput.value); // Extract name value
      }
  }

  // Send all data to the backend
  fetch("/custom/submit", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          table: tableData,
          colors: colors,
          names: names
      }),
  })
  .then(response => {
      if (!response.ok) {
          console.error("Failed to submit table data:", response.statusText);
      }
  })
  .catch(error => {
      console.error("Error while sending table data:", error);
  });
}
