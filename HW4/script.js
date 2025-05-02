function loadTruckingCompanies() {
  const jsonFileName = document.getElementById("jsonUrl").value;
  const errorMessage = document.getElementById("errorMessage");

  errorMessage.innerHTML = "";

  if (!jsonFileName) {
    errorMessage.innerHTML = "Please enter a JSON file name.";
    return;
  }

  fetch(`/myapp?file=${jsonFileName}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text(); // ✅ Expect HTML string
    })
    .then((html) => {
      const tableWindow = window.open(
        "",
        "",
        "width=800,height=600,scrollbars=yes"
      );
      if (tableWindow) {
        tableWindow.document.open();
        tableWindow.document.write(html); // ✅ Write the HTML string directly
        tableWindow.document.close();
      } else {
        errorMessage.innerHTML =
          "Popup blocked! Please allow popups for this site.";
      }
    })
    .catch((error) => {
      errorMessage.innerHTML = `Error: ${error.message}`;
    });
}
