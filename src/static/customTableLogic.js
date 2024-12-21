// generates a table with defined cols and rows
function generateTable() {
	const rows = document.getElementById("rows").value;
	const cols = document.getElementById("cols").value;

    if (isNaN(rows) || rows < 1 || rows > 10) {
        window.alert("invalid row count");
        return null;
    }

    if (isNaN(cols) || cols < 1 || cols > 7) {
        window.alert("invalid cols count");
        return null;
    }

	document.getElementById("matrixTable").innerHTML = "";

	const table = document.getElementById("matrixTable");
	for (let i = 0; i < rows; i++) {
		const row = table.insertRow();
		for (let j = 0; j < cols; j++) {
			const cell = row.insertCell();
			const input = document.createElement("input");
			input.type = "number";
			cell.appendChild(input);
		}
	}

    const submitButton = document.getElementById("submitButton");
    submitButton.style.display = "inline-block";
}





// add and remove rows from the risk settings
function addRow() {
	const table = document.getElementById("riskLevels").getElementsByTagName("tbody")[0];
	const rows = table.getElementsByTagName("tr");
	const newIndex = rows.length + 1;
	const newRow = document.createElement("tr");
	const numberCell = document.createElement("td");
	numberCell.innerText = newIndex;
	const colorCell = document.createElement("td");
	colorCell.innerHTML = '<input type="color" />';
	const nameCell = document.createElement("td");
	nameCell.innerHTML = '<input type="text" placeholder="Enter name" />';

	newRow.appendChild(numberCell);
	newRow.appendChild(colorCell);
	newRow.appendChild(nameCell);
	table.appendChild(newRow);

	updateIndexes();
}

function removeRow() {
	const table = document.getElementById("riskLevels").getElementsByTagName("tbody")[0];
	const rows = table.getElementsByTagName("tr");
	if (rows.length > 0) {
		table.deleteRow(rows.length - 1);
	}
}





// reads from the Risk Level Table
function extractRiskLevels() {
    const riskLevels = document.getElementById("riskLevels");
	const colorRows = riskLevels.getElementsByTagName("tbody")[0].rows;
	const colors = [];
	const riskNames = [];

	if (colorRows.length == 0) {
		window.alert("at least one Risk level required");
		return;
	}

	for (let i = 0; i < colorRows.length; i++) {
		const colorInput = colorRows[i].cells[1].querySelector("input[type='color']");
		const nameInput = colorRows[i].cells[2].querySelector("input[type='text']");
		if (colorInput) {
			colors.push(colorInput.value);
		}
		if (nameInput) {
			if (nameInput.value == "") {
				window.alert("name for every Risk Level required");
				return;
			}
			riskNames.push(nameInput.value);
		}
	}

    return [colors, riskNames];
}

// reads and checks Matrix Name
function extractMatrixName() {
	const name = document.getElementById("matrixName")

	if (name.value == "") {
		window.alert(`Please enter a matrix name`);
		return null
	}
	return name.value
}


// reads from the Matrix Representation Table
function extractMatrixTable(possibleRisks) {
    const matrixTable = document.getElementById("matrixTable");
    const numberRows = matrixTable.rows;
    const tableData = [];

    for (let i = 0; i < numberRows.length; i++) {
        const cells = numberRows[i].cells;
        const rowData = [];

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            const input = cell.querySelector("input");

            if (input) {
                const value = parseFloat(input.value);
                if (isNaN(value) || value > possibleRisks || value < 1) {
                    window.alert(`Invalid value in row ${i + 1}, column ${j + 1}.`);
                    return null; 
                }
                rowData.push(value);
            } else {
                window.alert(`Missing input in row ${i + 1}, column ${j + 1}.`);
                return null; 
            }
        }
        tableData.push(rowData);
    }

    return tableData;
}




// sends the gathered Matrix Data to the backend
function sendTableData() {
		matrixName = extractMatrixName();
		if (matrixName == null) {
			return null;
		}

    riskLevelData = extractRiskLevels();
    if (riskLevelData == null) {
        return null;
    }

    colors = riskLevelData[0];
    riskNames = riskLevelData[1];

    tableData = extractMatrixTable(colors.length);

    if (tableData == null) {
        return null;
    }

	fetch("/custom/enterTable", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			name: matrixName,
			table: tableData,
			colors: colors,
			riskNames: riskNames,
		}),
	})
		.then((response) => {
			if (!response.ok) {
				console.error("Failed to submit table data:", response.statusText);
			}
			else {
				window.alert("Risk Matrix successfully saved")
				const ulElement = document.querySelector("ul");
				const newLi = document.createElement("li"); 
				newLi.textContent = matrixName;
				ulElement.appendChild(newLi);
			}
		})
		.catch((error) => {
			console.error("Error while sending table data:", error);
		});
}
