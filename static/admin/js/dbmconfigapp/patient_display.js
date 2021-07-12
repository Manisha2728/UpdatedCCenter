$(document).ready(function() {
  $("#demographicsdetailsdegrid_set-group").css("margin", "0px 0");
  $("#clinicaldomainproperties_set-group").css("margin", "0px 0");
  $("#insurancedataelement_set-group").css("margin", "0px 0");
  $("#patientdetailssectionordering_set-group").css("margin", "0px 0");
  var headers = document.getElementsByTagName("thead");
  var th1 = headers[2].getElementsByTagName("th")[1];
  var th2 = headers[3].getElementsByTagName("th")[1];
  var th3 = headers[4].getElementsByTagName("th")[1];
  if (th1  && !th1.innerText.includes('Interpretation')) {
    th1.style.width = "78%";
    th1.innerText = "Elements";
  }
  if (th2  && !th1.innerText.includes('Interpretation')) {
    th2.style.width = "78%";
    th2.innerText = "Elements";
  }
  if (th3) {
    th3.style.width = "78%";
  }
});
