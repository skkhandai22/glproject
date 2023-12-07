$(document).ready(function () {
    // Default: Show email and survey containers, hide search container
    $('.search-container').hide();

    // Event listener for sidebar options
    $('ul').on('click', 'li a', function () {
        var option = $(this).text().trim().toLowerCase();

        // Show/hide containers based on the selected option
        switch (option) {
            case 'generate email':
                $('.search-container').hide();
                $('.email-container, .survey-container, #candidate-details').show();
                break;
            case 'find candidate':
                $('.email-container, .survey-container').hide();
                $('.search-container, #candidate-details').show();
                break;
            // Add more cases for additional options
        }
    });

    // Event listener for the search button
    $('#search-btn').on('click', function () {
        var email = $('#search-input').val();

        $.ajax({
            type: 'POST',
            url: '/eximius/api/getData/findcandidatedetail',
            contentType: 'application/json',
            data: JSON.stringify({ 'email': email }),
            success: function (response) {
                displayCandidateDetails(response);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    // Event listener for the generate button
    $('#generate-btn').on('click', function () {
        $.ajax({
            type: 'POST',
            url: '/eximius/api/candidate_onboarding_email',
            contentType: 'application/json',
            success: function (response) {
                // Update the email textarea with the generated email body
                $('#email-result').val(response.messageList[0].body);

                // Update the questionnaire form
                updateQuestionnaireForm(response.messageList[0].survey);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    // Function to display candidate details in a table
    function displayCandidateDetails(candidateDetails) {
        var detailsContainer = $('#candidate-details');
        detailsContainer.empty();

        if (candidateDetails.message.statusCode === 200) {
            var resumeRecord = candidateDetails.resumeRecord;
            var table = $('<table>').addClass('candidate-table');
            detailsContainer.append(table);

            for (var key in resumeRecord) {
                if (resumeRecord.hasOwnProperty(key)) {
                    var value = resumeRecord[key];

                    if (typeof value !== 'object') {
                        var row = $('<tr>');
                        row.append($('<td>').text(key));
                        row.append($('<td>').text(value));
                        table.append(row);
                    }
                }
            }
        } else {
            detailsContainer.text('No data found for the given candidate ID.');
        }
    }

    // Function to update the questionnaire form
    function updateQuestionnaireForm(survey) {
        var form = $('#survey-form');
        form.empty();

        var surveyTitle = $('<h3>').text(survey.surveyTitle);
        form.append(surveyTitle);

        for (var i = 0; i < survey.questions.length; i++) {
            var question = survey.questions[i];
            var questionText = $('<p>').text(question.questionText);
            form.append(questionText);

            switch (question.responseType) {
                case 'ratings':
                    var ratingsInput = $('<select>').attr('name', 'question' + (i + 1));
                    for (var j = 0; j < question.responseOptions.length; j++) {
                        ratingsInput.append($('<option>').text(question.responseOptions[j]));
                    }
                    form.append(ratingsInput);
                    break;
                case 'Binary':
                    var binaryInput = $('<select>').attr('name', 'question' + (i + 1));
                    for (var k = 0; k < question.responseOptions.length; k++) {
                        binaryInput.append($('<option>').text(question.responseOptions[k]));
                    }
                    form.append(binaryInput);
                    break;
                case 'user input':
                    var userInput = $('<input>').attr({ type: 'text', name: 'question' + (i + 1), placeholder: 'Your Answer' });
                    form.append(userInput);
                    break;
            }
        }
    }
});
