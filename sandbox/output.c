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
  if (x[1] <= 0.0101689459) {
    if (x[2] <= -3.3597506285) {
      return CompressPAA;
    }
    else {
      if (x[1] <= 0.0094248354) {
        return CompressNTHS;
      }
      else {
        if (x[2] <= -0.8680301905) {
          return CompressNTHS;
        }
        else {
          return CompressByChunk;
        }
      }
    }
  }
  else {
    if (x[2] <= -1.5283702016) {
      if (x[2] <= -1.5675927401) {
        return CompressPAAVI;
      }
      else {
        return CompressMinMax;
      }
    }
    else {
      if (x[2] <= -0.7599598598) {
        return CompressByChunk;
      }
      else {
        if (x[1] <= 0.0138551458) {
          return CompressAPCADFT;
        }
        else {
          return CompressByChunk;
        }
      }
    }
  }
};
