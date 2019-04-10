
// Adding the .format() function to String prototype
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

/*
This function colors the hashes and prev hashes of each block an appropriate color.
If the prevHash of a block matches the hash of the previous block, then both
will appear green (by adding a Bootstrap class to the cell). If there's a
mismatch, then both will appear red.
*/
document.addEventListener("DOMContentLoaded", function(event) {
    var numBlocks = window.CONFIG.numBlocks;
    // For each cell:
    for (var i = 1; i < numBlocks; i++) {
        var blockTableId = "block-{0}-table".format(i);
        var prevBlockTableId = "block-{0}-table".format(i-1);

        var prevHashTd = $('#' + blockTableId).find("td.prev-hash");
        var prevBlockHashTd = $('#' + prevBlockTableId).find("td.hash");

        if (prevHashTd.text() === prevBlockHashTd.text()){
            var classToAdd = "table-success";
        }
        else{
            var classToAdd = "table-danger";
        }
        prevHashTd.addClass(classToAdd);
        prevBlockHashTd.addClass(classToAdd);
    }
});
