/*
   Copyright 2021 FogML

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

int classifier(double * x){
  if (x[62] <= 0.3027277291) {
    if (x[55] <= 0.7238609344) {
      if (x[60] <= -0.0161668435) {
        return CompressAPCADFT;
      }
      else {
        if (x[54] <= -0.0374071077) {
          return CompressPIP_PD;
        }
        else {
          return CompressByChunk;
        }
      }
    }
    else {
      return CompressPIP_ED;
    }
  }
  else {
    return CompressSTC;
  }
};
