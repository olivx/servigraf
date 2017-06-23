$(function(){

    function loadClientForm(){
         var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'GET',
            dataType: 'json',
            beforeSend: function(){
                $('#cliente-modal').modal('show');
            },
            success: function(data){
                $('#cliente-modal .modal-content').html(data.html_form);
            }
        });
    };

    function saveClientForm(){  


        form =  $(this);
            $.ajax({

                url:  form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(),
                dataType: 'json',

                success: function(data){
                    if(data.is_form_valid){

                        $('#cliente-table tbody').html(data.html_table);
                        $('#cliente-modal').modal('hide');
                        alert(data.message)

                    }else{
                        alert(data.message)
                        $('#cliente-modal .modal-content').html(data.html_form);
                    }

                }
    });

    return false;
};

    $("#cliente-modal").on("shown.bs.modal", function (e) {

        $('select').on('change', function(){
            var _select = $(this);
            if(_select.val() == 2){
                $('[href="#section-contact"]').closest('li').hide();
                $('form').find('#div-razao-social label').text('Nome:');
                $('form').find('#div-nome-fantasia label').text('Sobre Nome:');
                $('form').find('#div-documento label').text('CPF:');


            }else{
                $('[href="#section-contact"]').closest('li').show();
                $('form').find('#div-razao-social label').text('Razão Social:');
                $('form').find('#div-nome-fantasia label').text('Nome Fantasia:');
                $('form').find('#div-documento label').text('CNPJ:');
            }
        });
    });


    // save cliente form
    $('.js-open-form-cliente').click(loadClientForm);
    $('#cliente-modal').on('submit', '.js-save-client-form', saveClientForm);

    // update cliente form
    $('#cliente-table').on('click' , '.js-update-modal-cliente', loadClientForm);
    $('#cliente-modal').on('submit', '.js-update-client-form', saveClientForm);

    // delete client
    $('#cliente-table').on('click', '.js-delete-modal-cliente', loadClientForm);
    $('#cliente-modal').on('submit', '.js-delete-client-form', saveClientForm);


});