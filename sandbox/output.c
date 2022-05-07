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
  if (x[1] <= 0.0132601527) {
    if (x[1] <= 0.0094882352) {
      if (x[2] <= -2.0584602356) {
        return CompressPIP_PD_0.2;
      }
      else {
        return CompressPIP_VD_0.2;
      }
    }
    else {
      if (x[1] <= 0.0104780667) {
        return CompressMinMax_0.1;
      }
      else {
        if (x[1] <= 0.0109610641) {
          return CompressPWP_0.3;
        }
        else {
          return CompressMinMax_0.1;
        }
      }
    }
  }
  else {
    if (x[1] <= 0.0154281938) {
      return CompressPIP_PD_0.1;
    }
    else {
      if (x[1] <= 0.0185973477) {
        return CompressMinMax_0.2;
      }
      else {
        return CompressPIP_ED_0.1;
      }
    }
  }
};
