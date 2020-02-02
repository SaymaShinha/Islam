var topContainer = $("#top-widget");
var topTrigger = $("#top-open");

topTrigger.click(function () {
    topContainer.animate({
        height: 'toggle'
    });

    if (topTrigger.hasClass('tab-closed')) {
        topTrigger.removeClass('tab-closed');
    } else {
        topTrigger.addClass('tab-closed');
    }

    return false;

});


// Create the dropdown base
$("<select id='comboNav' />").appendTo("#combo-holder");

// Create default option "Go to..."
$("<option />", {
    "value": "",
    "text": "Navigation"
}).appendTo("#combo-holder select");

$("#nav a").each(function () {
    var el = $(this);
    var label = $(this).parent().parent().attr('id');
    var selected_option = $(this).parent().attr('class');
    var sub = (label == 'nav') ? '' : '- ';

    if (selected_option === "current-menu-item") {
        $("<option />", {
            "value": el.attr("href"),
            "text": sub + el.text(),
            "selected": "selected"
        }).appendTo("#combo-holder select");
    } else {
        $("<option />", {
            "value": el.attr("href"),
            "text": sub + el.text(),
        }).appendTo("#combo-holder select");
    }
});

$("#comboNav").change(function () {
    location = this.options[this.selectedIndex].value;
});
