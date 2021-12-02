

$(function(){
    tinymce.init({
        selector:'#post',
        height:500,
        plugins:"quickbars emoticons",
        inline: false,
        toolbar: true,
        menubar : true,
        quickbars_selection_toolbar:'bold italic | link h2 h3 blockquote',
        quickbars_insert_toolbar: 'quickimage quicktable',
    })


});