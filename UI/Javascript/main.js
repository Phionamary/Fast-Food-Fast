function SelectUser() {
  var user_role = document.getElementById("id")

  if (user_role.value === "radioadmin"){
    window.location.href = "UI/admin.html";
    return false
  }

  else if(user_role.value === "radiouser"){
    window.location.href = "UI/orders.html";
    return false
  }

  }