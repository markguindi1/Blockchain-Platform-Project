
/*
This function colors the hashes and prev hashes of each block an appropriate color.
If the prevHash of a block matches the hash of the previous block, then both
will appear green (by adding a Bootstrap class to the cell). If there's a
mismatch, then both will appear red.
*/

var colorAllHashes = function(blockchains) {
    // For each blockchain on the page:
    for (var bcId in blockchains){
        var numBlocks = blockchains[bcId].numBlocks;
        colorBlockchainHashes(bcId, numBlocks);
    }
}

var colorBlockchainHashes = function(bcId, numBlocks){
  // For each block on the blockchain:
  for (var i = 1; i < numBlocks; i++) {
      // Get Id's of each block's table
      var blockTableId = getBlockTableId(bcId, i);
      var prevBlockTableId = getBlockTableId(bcId, i-1);

      // Get actual cells with the hash and previousHash we're comparing
      var $prevHashTd = $('#' + blockTableId).find("td.prev-hash");
      var $prevBlockHashTd = $('#' + prevBlockTableId).find("td.hash");

      // Compare them, and change
      if ($prevHashTd.text() === $prevBlockHashTd.text()){
          var classToAdd = "table-success";
          var classToRemove = "table-danger";
      }
      else{
          var classToAdd = "table-danger";
          var classToRemove = "table-success";
      }

      $prevHashTd.addClass(classToAdd);
      $prevHashTd.removeClass(classToRemove);

      $prevBlockHashTd.addClass(classToAdd);
      $prevBlockHashTd.removeClass(classToRemove);
  }
}

document.addEventListener("DOMContentLoaded", function(event){
  var blockchains = window.CONFIG.blockchains;
  colorAllHashes(blockchains);
});
