
/*
Utility functions
*/

// Adding the .format() function to String prototype
String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
};

var getBlockchainTableId = function(bcId){
  return "{0}-table".format(bcId);
}

var getBlockTableId = function(bcId, blockI){
  return "{0}-{1}-table".format(bcId, blockI);
}

var getBlockRowId = function(bcId, blockI){
  return "{0}-{1}-row".format(bcId, blockI);
}

var getBlockNumberCellId = function(bcId, blockI){
  return "{0}-{1}-block-i".format(bcId, blockI);
}
