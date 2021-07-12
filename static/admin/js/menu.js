function expand_collapse_submenu(id) {
    var submenu = document.getElementById(id)
    if (submenu.style.display == "none")
        submenu.style.display = "block";
    else
        submenu.style.display = "none";
}