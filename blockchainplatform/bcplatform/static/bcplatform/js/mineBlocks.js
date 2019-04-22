
// For each blockchain:
  // every x seconds:
  // Mine block (through AJAX call)
  // If HTML not on page yet, add it to page (hidden)
  // Populate HTML
  // If HTML hidden, display (using effect)

var createMiningEventHandlers = function(event) {
  var blockchains = window.CONFIG.blockchains;
    var timeoutMs = 10 * 1000;

    // For each blockchain on the page:
    for (var bcId in blockchains){
        var numBlocks = blockchains[bcId].numBlocks;
        var intervalMs = blockchains[bcId].intervalMs;
        // Add event listener for mineBlockchainForInterval on when page loads
        document.addEventListener("DOMContentLoaded", function(event){
          mineBlockchainForInterval(bcId, intervalMs, timeoutMs)
        });
    }
}

var mineBlockchainForInterval = function(bcId, intervalMs, timeoutMs){
  var startTime = new Date().getTime();

  // Mine block on interval
  var interval = setInterval(function(){
    if(new Date().getTime() - startTime > timeoutMs){
      clearInterval(interval);
      return;
    }
    // Get block index to mine from CONFIG (which is updatred by the
    // mineBlockchainBlock function after each block is mined)
    var blockchains = window.CONFIG.blockchains;
    var blockI = blockchains[bcId].numBlocks;
    mineBlockchainBlock(bcId, blockI);
  }, intervalMs);
}

var mineBlockchainBlock = function(bcId, blockI){
  var url = "/blockchain/rest/mine-block/{0}/{1}/".format(bcId, blockI);
  $.getJSON(url, function(data){
    // If HTML not on page yet, add it to page (hidden)
    var bcId = data.chain_pk;
    var blockI = data.index;

    var minedBlockTableId = getBlockTableId(bcId, i);
    var $minedBlockTable = $("#" + minedBlockTable);
    // If element does not exist:
    if (! $minedBlockTable.length){
      var $minedBlockTable = addBlockHTMLToPage(bcId, blockI);
    }
    // Empty block
    emptyBlockHTML(bcId, blockI);

    // Populate HTML
    populateBlockHTML(bcId, blockI, data);

    // If HTML hidden, display (using effect)
    $minedBlockTable.show()

    // Update numBlocks
    window.CONFIG.blockchains[bcId].numBlocks++;

    // Recolor Blockchain hashes
    colorBlockchainHashes(bcId, window.CONFIG.blockchains[bcId].numBlocks);

  });
};

var addBlockHTMLToPage = function(bcId, blockI){
  // Add element to page
  var genesisBlockTableId = getBlockTableId(bcId, 0);
  var blockchainTableId = getBlockchainTableId(bcId);
  var $newBlockTable = $("#" + genesisBlockTableId)
    .clone() // Clone block table
    .prop('id', getBlockTableId(bcId, blockI)) // Set new block table id to correct id
    .prependTo("#" + blockchainTableId) // Prepend to blockchain table
    .hide(); // Hide new block table

  return $newBlockTable;
};

var emptyBlockHTML = function(bcId, blockI){
  // Empty cells
  var $minedBlockTable = $("#" + getBlockTableId(bcId, blockI));

  $minedBlockTable.find("td").each(function(){
    var $dataTextarea = $(this).find("textarea");
    if ($dataTextarea.length){
        $dataTextarea.empty();
    }
    else {
        $(this).empty();
    }
  });
}

var populateBlockHTML = function(bcId, blockI, data){
  var $minedBlockTable = $("#" + getBlockTableId(bcId, blockI));
  $minedBlockTable.find("td.hash").append(data.hash);
  $minedBlockTable.find("td.timestamp").append(data.timestamp);
  $minedBlockTable.find("td.nonce").append(data.nonce);
  $minedBlockTable.find("td.prev-hash").append(data.previous_hash);
  $minedBlockTable.find("td.data").find("textarea").append(data.data);
};

/*
Example data from REST endpoint:
{
  "chain_pk": 39,
  "data": "If Java had true garbage collection, most programs would delete themselves upon execution.",
  "index": 30,
  "timestamp": "2019-04-22T04:12:51.367Z",
  "previous_hash": "00436986afe2af6b8d42ffccd0bc22bba6aae7d750f9ce1030fc1e3e52539db5",
  "nonce": "199",
  "hash": "0098eaa6c6a1af99745234c40beba4d2281096065c1d35443e080dee31584946"
}
*/
