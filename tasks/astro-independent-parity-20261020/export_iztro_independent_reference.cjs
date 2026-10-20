#!/usr/bin/env node
/**
 * Independent chart generation for already frozen synthetic date grid.
 * Requires pinned iztro@2.6.3 external node_modules via NODE_PATH.
 * Source-lane Python mechanics are not imported; no real human outcomes.
 */
'use strict';
const fs=require('fs');
const crypto=require('crypto');
const path=require('path');
const {astro}=require('iztro');
const pkg=require('iztro/package.json');
const [inputPath,outputPath]=process.argv.slice(2);
if(!inputPath || !outputPath)throw new Error('Need input.json output.json');
if(pkg.version!=='2.6.3')throw new Error('Pinned iztro package version mismatch');
const inputRaw=fs.readFileSync(inputPath);
const inputSha=crypto.createHash('sha256').update(inputRaw).digest('hex');
if(inputSha!=='cbad83855602700f6835b3ff48e2a27f4868575e6e2e8de46a3e1a80d73f8299')
 throw new Error('Frozen pre-reference input SHA drift');
const input=JSON.parse(inputRaw.toString('utf8'));
if(input.cases.length!==1354)throw new Error('Frozen grid size drift');
const NAMES=new Set(['紫微','天机','太阳','武曲','天同','廉贞','天府','太阴','贪狼','巨门','天相','天梁','七杀','破军']);
function starMap(c){
 const o={};
 for(const palace of c.palaces){
  if(typeof palace.earthlyBranch!=='string')throw new Error('Missing birthplace palace string');
  for(const st of palace.majorStars){
   if(!NAMES.has(st.name))throw new Error('Unknown major star '+st.name);
   if(o[st.name])throw new Error('Duplicate major star '+st.name);
   o[st.name]=palace.earthlyBranch;
  }
 }
 if(Object.keys(o).length!==14)throw new Error('Expected 14 original major stars');
 return o;
}
const results=[];
for(let i=0;i<input.cases.length;i++){
 const fixture=input.cases[i];
 const c=astro.bySolar(fixture.solar_date_for_Iztro,
   fixture.timeIndex_0_to_12,fixture.sex_for_Iztro_required_field_but_not_main_star_placement,
   true,'zh-CN');
 results.push({
   index:i,
   synthetic_label:fixture.synthetic_label,
   input_split:fixture.split,
   input_fixed_CST:fixture.local_CST_fixed_timestamp,
   input_solar_date:fixture.solar_date_for_Iztro,
   hour_index_used:fixture.timeIndex_0_to_12,
   date_clock_minutes_not_representable_by_iztro:fixture.calendar_clock_minutes_discarded_by_iztro_hour_branch_API,
   reference_chart_four_pillars:c.chineseDate,
   lunar_date_human_readable_chinese:c.lunarDate,
   reference_bureau:c.fiveElementsClass,
   reference_life_branch:c.earthlyBranchOfSoulPalace,
   reference_body_branch:c.earthlyBranchOfBodyPalace,
   fourteen_major_star_original_chinese_name_to_palace:starMap(c)
 });
}
const packageLock=path.resolve(path.dirname(require.resolve('iztro/package.json')),'../../package-lock.json');
const packageLockBytes=fs.existsSync(packageLock)?fs.readFileSync(packageLock):null;
const lock=packageLockBytes?JSON.parse(packageLockBytes.toString('utf8')):null;
const output={
 schema:'IZTRO_2_6_3_EXTERNAL_INDEPENDENT_SYNTHETIC_CHART_GRID_V1',
 third_party_implementation:'SylarLong/iztro (separate TypeScript/JavaScript calculator)',
 independent_library_version:pkg.version,
 package_lock_sha256:packageLockBytes?crypto.createHash('sha256').update(packageLockBytes).digest('hex'):null,
 npm_package_tarball_integrity:lock?.packages?.['node_modules/iztro']?.integrity||null,
 frozen_input_manifest_sha256:inputSha,
 synthetic_input_count:results.length,
 reference_gender_for_structure_only:'male',
 reference_fixLeap:true,
 hour_time_quantized_to_2h_in_reference:true,
 modern_algorithm_not_classical_Ming_source_authentication:true,
 real_human_response_outcomes_scored:0,
 runtime_astrological_rules_promoted:0,
 outputs:results
};
const data=JSON.stringify(output,null,2)+'\n';
fs.writeFileSync(outputPath,data,{encoding:'utf8',flag:'wx'});
console.log(JSON.stringify({n:results.length,version:pkg.version,inputSha,
  outputSha:crypto.createHash('sha256').update(data).digest('hex'),
  packageIntegrity:output.npm_package_tarball_integrity},null,2));
