function deleteReport(reportId) {
  fetch("/delete-report", {
    method: "POST",
    body: JSON.stringify({ reportId: reportId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
