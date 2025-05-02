function showTab(id) {
  // Hide all tab content
  document
    .querySelectorAll(".tab-content")
    .forEach((tab) => (tab.style.display = "none"));

  // Remove 'active' from all buttons
  document
    .querySelectorAll(".tabs button")
    .forEach((btn) => btn.classList.remove("active"));

  // Show selected tab content
  document.getElementById(id).style.display = "block";

  // Highlight selected tab button
  const btns = {
    outlook: 0,
    summary: 1,
    history: 2,
  };
  document.querySelectorAll(".tabs button")[btns[id]].classList.add("active");
}

function clearFields() {
  document.getElementById("ticker").value = "";
  document.getElementById("outlook").innerHTML = "";
  document.getElementById("summary").innerHTML = "";
  document.getElementById("message").innerText = "";
}

async function searchStock() {
  const ticker = document.getElementById("ticker").value.trim();
  if (!ticker) {
    alert("Please fill out stock tiker field");
    return;
  }

  try {
    const res = await fetch(`http://127.0.0.1:5000/search?ticker=${ticker}`);
    const data = await res.json();
    if (data.error) {
      document.getElementById("message").innerText = data.error;
      return;
    }

    document.getElementById("message").innerText = data.from_cache
      ? "Served from cache"
      : "";
    displayOutlook(data.company);
    displaySummary(data.stock);
    showTab("outlook");
  } catch (err) {
    document.getElementById("message").innerText = "An error occurred.";
  }
}

function displayOutlook(company) {
  document.getElementById("outlook").innerHTML = `
      <table>
        <tr><td>Company Name</td><td>${company.name}</td></tr>
        <tr><td>Ticker</td><td>${company.ticker}</td></tr>
        <tr><td>Exchange</td><td>${company.exchangeCode}</td></tr>
        <tr><td>Start Date</td><td>${company.startDate}</td></tr>
        <tr><td>Description</td><td>${company.description.slice(
          0,
          500
        )}...</td></tr>
      </table>
    `;
}

function displaySummary(stock) {
  const change = (stock.last - stock.prevClose).toFixed(2);
  const changePercent = ((change / stock.prevClose) * 100).toFixed(2);
  const arrowSrc =
    change >= 0 ? "../static/GreenArrowUP.png" : "../static/RedArrowDown.png";

  document.getElementById("summary").innerHTML = `
      <table>
        <tr><td>Ticker</td><td>${stock.ticker}</td></tr>
        <tr><td>Date</td><td>${stock.timestamp.split("T")[0]}</td></tr>
        <tr><td>Prev Close</td><td>${stock.prevClose}</td></tr>
        <tr><td>Open</td><td>${stock.open}</td></tr>
        <tr><td>High</td><td>${stock.high}</td></tr>
        <tr><td>Low</td><td>${stock.low}</td></tr>
        <tr><td>Last</td><td>${stock.last}</td></tr>
        <tr><td>Change</td><td>${change} <img src="${arrowSrc}" alt="arrow" width="15"</td></tr>
        <tr><td>Change %</td><td>${changePercent}% <img src="${arrowSrc}" alt="arrow" width="15"</td></tr>
        <tr><td>Volume</td><td>${stock.volume}</td></tr>
      </table>
    `;
}

async function loadHistory() {
  const res = await fetch("http://127.0.0.1:5000/history");
  const history = await res.json();
  const tableRows = history
    .map((row) => `<tr><td>${row.ticker}</td><td>${row.timestamp}</td></tr>`)
    .join("");
  document.getElementById(
    "history"
  ).innerHTML = `<table><tr><th>Ticker</th><th>Timestamp</th></tr>${tableRows}</table>`;
  showTab("history");
}
