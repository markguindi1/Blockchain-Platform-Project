
// For each blockchain:
  // every x seconds:
  // Mine block (through AJAX call)
  // If HTML not on page yet, add it to page (hidden)
  // Populate HTML
  // If HTML hidden, display (using effect)

var createMiningEventHandlers = function() {
  window.CONFIG = CONFIG;
  var blockchains = window.CONFIG.blockchains;
  var timeoutMs = window.CONFIG.timeoutMs;
  var bcIdArray = [];

  // Add bcIds to array
  for (var bcId in window.CONFIG.blockchains){
    bcIdArray.push(bcId);
  }

  // forEach is used so the event listener uses the current value of bcId, not
  // the last value.
  bcIdArray.forEach(function(bcId){
    var numBlocks = blockchains[bcId].numBlocks;
    var intervalMs = blockchains[bcId].intervalMs;
    // Add event listener for mineBlockchainForInterval on when page loads
    document.addEventListener("DOMContentLoaded", function(event){
      mineBlockchainForInterval(bcId, intervalMs, timeoutMs);
      console.log("I'm here, bcId is " + bcId);
      // mineBlockchainOnce(bcId);
    });
  });
}

// Used for development/testing only
var mineBlockchainOnce = function(bcId){
  // Get block index to mine from CONFIG (which is updated by the
  // mineBlockchainBlock function after each block is mined)
  var blockchains = window.CONFIG.blockchains;
  var blockI = blockchains[bcId].numBlocks;
  mineBlockchainBlock(bcId, blockI);
}

var mineBlockchainForInterval = function(bcId, intervalMs, timeoutMs){
  var startTime = new Date().getTime();

  // Mine block on interval
  var interval = setInterval(function(){
  // var interval = setTimeout(function(){
    if(new Date().getTime() - startTime > timeoutMs){
      clearInterval(interval);
      // clearTimeout(interval);
      return;
    }
    // Get block index to mine from CONFIG (which is updated by the
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

    var minedBlockRowId = getBlockRowId(bcId, blockI);
    var $minedBlockRow = $("#" + minedBlockRowId);
    // If element does not exist:
    if (! $minedBlockRow.length){
      $minedBlockRow = addBlockHTMLToPage(bcId, blockI);
    }
    // Empty block
    emptyBlockHTML(bcId, blockI);

    // Populate HTML
    populateBlockHTML(bcId, blockI, data);

    // If HTML hidden, display (using effect)
    $minedBlockRow.show()

    // Update numBlocks
    window.CONFIG.blockchains[bcId].numBlocks++;

    // Recolor Blockchain hashes
    colorBlockchainHashes(bcId, window.CONFIG.blockchains[bcId].numBlocks);

  });
};

var addBlockHTMLToPage = function(bcId, blockI){
  // Add element to page
  var genesisBlockRowId = getBlockRowId(bcId, 0);
  var blockchainTableId = getBlockchainTableId(bcId);
  var newBlockNumberCellId = getBlockNumberCellId(bcId, blockI);
  var newBlockRowId = getBlockRowId(bcId, blockI);
  var newBlockTableId = getBlockTableId(bcId, blockI);
  var $blockchainTable = $("#" + blockchainTableId);
  var $newBlockRow = $("#" + genesisBlockRowId)
    .clone() // Clone block row
    .prependTo($blockchainTable.find("tbody.blockchain-tbody")) // Prepend to blockchain table body
    .prop('id', newBlockRowId) // Set new block row id to correct id
    .hide(); // Hide new block row

  // Set new block table id to correct id
  $newBlockRow.find("table").prop('id', newBlockTableId);
  // Set new block "Block #" cell id to correct id
  $newBlockRow.find(".block-i").prop('id', newBlockNumberCellId);

  return $newBlockRow;
};

var emptyBlockHTML = function(bcId, blockI){
  // Empty cells
  var $minedBlockRow = $("#" + getBlockRowId(bcId, blockI))
    .find("th" + "#" + getBlockNumberCellId(bcId, blockI))
    .empty();

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

  var $minedBlockRow = $("#" + getBlockRowId(bcId, blockI))
    .find("th" + "#" + getBlockNumberCellId(bcId, blockI))
    .append(data.index);

  var $minedBlockTable = $("#" + getBlockTableId(bcId, blockI));
  $minedBlockTable.find("td.hash").append(data.hash);
  $minedBlockTable.find("td.timestamp").append(data.timestamp);
  $minedBlockTable.find("td.nonce").append(data.nonce);
  $minedBlockTable.find("td.prev-hash").append(data.previous_hash);
  $minedBlockTable.find("td.data").find("textarea").append(data.data);
};

createMiningEventHandlers();
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
