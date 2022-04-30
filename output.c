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
  if (x[9] <= 0.1900000051) {
    if (x[15] <= 0.9054305553) {
      return CompressMinMax;
    }
    else {
      return CompressPIP_ED;
    }
  }
  else {
    if (x[5] <= -1.3726827502) {
      return CompressSTC;
    }
    else {
      if (x[2] <= -126.7160949707) {
        return CompressSTC;
      }
      else {
        return CompressHigherDeriveration;
      }
    }
  }
};
