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
  if (x[1] <= 0.0085280617) {
    if (x[2] <= -1.2784000635) {
      return CompressPWP_0.6;
    }
    else {
      return CompressPWP_0.2;
    }
  }
  else {
    if (x[1] <= 0.0127517413) {
      if (x[2] <= -1.7162283659) {
        return CompressPWP_0.1;
      }
      else {
        return CompressMinMax_0.1;
      }
    }
    else {
      if (x[2] <= -0.5584419416) {
        return CompressMinMax_0.5;
      }
      else {
        if (x[2] <= -0.0099164294) {
          return CompressMinMax_0.2;
        }
        else {
          return CompressPWP_0.1;
        }
      }
    }
  }
};
