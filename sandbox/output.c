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
  if (x[1] <= 0.0109456773) {
    if (x[1] <= 0.0049999999) {
      return CompressPIP_ED_0.3;
    }
    else {
      return CompressMinMax_0.1;
    }
  }
  else {
    if (x[2] <= -2.2277358174) {
      return CompressPIP_ED_0.4;
    }
    else {
      if (x[1] <= 0.0126595069) {
        return CompressPIP_PD_0.1;
      }
      else {
        if (x[1] <= 0.0137926689) {
          return CompressPIP_VD_0.1;
        }
        else {
          if (x[2] <= -1.6027950048) {
            return CompressPIP_ED_0.3;
          }
          else {
            if (x[2] <= -0.7079290533) {
              return CompressPIP_ED_0.5;
            }
            else {
              return CompressMinMax_0.2;
            }
          }
        }
      }
    }
  }
};
