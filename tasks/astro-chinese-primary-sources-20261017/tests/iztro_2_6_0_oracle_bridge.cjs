"use strict";
/* Optional external, pinned iztro v2.6.0 chart readback. NO copied vendor code.
 * IO: JSON {cases:[{id,lunar_ymd,time_index,gender,leap,fix_leap}]} stdin.
 * Output: one JSON {version,config,results:[{id,life,body,bureau,stars,...}]} stdout.
 */
const fs = require("fs");
const path = require("path");
const packageDir = process.env.IZTRO_MODULE_DIR;
if (!packageDir || !path.isAbsolute(packageDir)) {
  throw new Error("IZTRO_MODULE_DIR must be an explicit absolute optional package directory");
}
const pkg = require(path.join(packageDir, "package.json"));
if (pkg.version !== "2.6.0") throw new Error("Unexpected iztro package version: " + pkg.version);
const { astro } = require(packageDir);
const config = astro.getConfig();
if (config.algorithm !== "default" || config.yearDivide !== "normal"
    || config.dayDivide !== "forward" || config.horoscopeDivide !== "normal") {
  throw new Error("Unexpected modern iztro source conventions: " + JSON.stringify(config));
}
const input = JSON.parse(fs.readFileSync(0, "utf8"));
if (!Array.isArray(input.cases)) throw new Error("Expected cases array");
const results = input.cases.map(c => {
  if (!Number.isInteger(c.time_index) || c.time_index < 0 || c.time_index > 11
      || !["male","female"].includes(c.gender)
      || typeof c.leap !== "boolean" || typeof c.fix_leap !== "boolean") {
    throw new Error("Unrecognized manual source-chart test input: " + JSON.stringify(c));
  }
  const chart = astro.byLunar(c.lunar_ymd,c.time_index,c.gender,c.leap,c.fix_leap,"zh-CN");
  const starPalaces = {};
  let count = 0;
  const names = {};
  for (const palace of chart.palaces) {
    for (const star of palace.majorStars) {
      if (star.name in starPalaces) throw new Error("Duplicate principal star " + star.name);
      starPalaces[star.name] = palace.earthlyBranch;
      count += 1;
    }
    names[palace.earthlyBranch] = palace.name;
  }
  if (count !== 14 || Object.keys(names).length !== 12) {
    throw new Error("Unexpected iztro v2.6.0 principal-star count or palace count");
  }
  return {
    id:c.id,
    solar_date:chart.solarDate,
    lunar_date_chinese:chart.lunarDate,
    life_palace:chart.earthlyBranchOfSoulPalace,
    body_palace:chart.earthlyBranchOfBodyPalace,
    five_element_bureau:chart.fiveElementsClass,
    star_palaces:starPalaces,
    gender:chart.gender,
    all_12_palace_names:names
  };
});
process.stdout.write(JSON.stringify({
  outside_provider:"SylarLong/iztro",
  pinned_version:pkg.version,
  original_license_or_dependency_copied:false,
  source:"https://github.com/SylarLong/iztro",
  source_study_independence:"external software implementation, not original ancient manuscript or human proof",
  config:{
    yearDivide:config.yearDivide,
    dayDivide:config.dayDivide,
    algorithm:config.algorithm,
    horoscopeDivide:config.horoscopeDivide
  },
  cases:results
}));
