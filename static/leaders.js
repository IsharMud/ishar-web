if (window.location.search != '?dead=false') {
    document.getElementById('include-dead').checked = true;
} else {
    document.getElementById('include-dead').checked = false;
};

function deadLeaders(value) {
    if ((value == false) && (window.location.search != '?dead=false')) {
        window.location.search = '?dead=false';
    };
    if (value == true) {
        window.location.search = '';
    };
};
