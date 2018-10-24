function showPost() {
$('#postCreater').css('top', '10%');
$('#scrim').css('display', 'inline-block');
}

function scrimTriger(caseNum) {
  switch (caseNum) {
    case 1:
      hidePost();
      break;
    default:
      hidePost();
  }
}

function hidePost() {
  $('#postCreater').css('top', '-100%');
  $('#scrim').css('display', 'none');
}

function submitForm(status) {

  $('#formStatus').val(status);
  $('#subButton').click();

}


function selectTag(tag) {
  var span =tag.getElementsByTagName("span")[0];
  var showDelete = tag.getElementsByClassName("removeImg")[0];
  showDelete.select = "true";
  showDelete.style.display = "block";
}
