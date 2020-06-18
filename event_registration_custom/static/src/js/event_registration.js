odoo.define('event_registration_custom.event_registration', function (require) {

var ajax = require('web.ajax');
var core = require('web.core');
var Widget = require('web.Widget');
var publicWidget = require('web.public.widget');

var _t = core._t;

    $(document).on('click','button.btn-form',function(ev){
        ev.preventDefault();
        ev.stopImmediatePropagation();
        var valid = true;
        var form = ev.target.closest('form');
        var emails = [];
        var repeated_emails = [];
        var inputs_emails = $(form).find('input[type=email]');
        var selected_options = $(form).find('option:selected');
        $(form).find('.invalid-answer').remove();
        var answer_ids = [];
        var answer_elem = {};
        var empty = $(form).find('input[required]').filter(function() {
            return this.value == '';
        });
        if (empty.length) {
            valid = false;
            alert('enter all required field!');
        }

        for(var i = 0 ; i < inputs_emails.length ; i ++){
            var inpt = inputs_emails[i];
            var val = inpt.value;
            if(emails.includes(val)){
                repeated_emails.push(val);
            }else{
                emails.push(val);
            }
        }
        for(var j = 0 ; j < selected_options.length ; j ++){
            var option = selected_options[j];
            var val = parseInt(option.value);
            answer_ids.push(val);
            answer_elem[val] = option;
        }

        if(repeated_emails.length){
            valid = false;
            var repeated_str = repeated_emails.join(' - ');
            alert('You are already registered under ' + repeated_str + ' for this event.. Maximum 1 registration per person is allowed.');
        }else{
            var form_action = form['action'];
            var event_str = form_action.split('/')[4];
            var url = '/event/' + event_str + '/check_attendees_data'
            ajax.jsonRpc(url, 'call', {'emails':emails,'answers':answer_ids}).then(function(res) {
                if(res){
                    var repeated_emails = res['emails'];
                    var invalid_answers = res['answers'];
                    if(repeated_emails.length){
                        var repeated_str = repeated_emails.join(' - ');
                        valid = false;
                        alert('You are already registered under ' + repeated_str + ' for this event .. Maximum 1 registration per person is allowed.');
                    }
                    if(invalid_answers.length){
                        valid = false;
                        for(var k = 0 ; k < invalid_answers.length ; k++){
                            var option = answer_elem[invalid_answers[k]];
                            $($(option).parent()).after('<span="invalid-error" style="color:red;" class="invalid-answer">With this answer you are not eligible to Register.</span>');;
                        }
                    }

                }
                if(valid){
                    $(form).submit();
                }
            });
        }

    })

})