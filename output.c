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
  if (x[1] <= 0.0049487797) {
    return CompressNTHS;
  }
  else {
    if (x[2] <= -1.6061705947) {
      return CompressHigherDeriveration;
    }
    else {
      if (x[2] <= -0.4879163019) {
        return CompressSTC;
      }
      else {
        if (x[1] <= 0.0096296482) {
          return CompressHigherDeriveration;
        }
        else {
          if (x[1] <= 0.0130294086) {
            return CompressMinMax;
          }
          else {
            return CompressPIP_ED;
          }
        }
      }
    }
  }
};
