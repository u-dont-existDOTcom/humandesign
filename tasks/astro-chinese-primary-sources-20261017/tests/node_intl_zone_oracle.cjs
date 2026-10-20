"use strict";
/* Independent ECMAScript Intl projection of UTC instants into named IANA
 * local clocks. No timezone data or vendor runtime copied to repository.
 * Test-only external implementation comparator; not proof of historical tzdb.
 */
const fs = require("fs");
const input = JSON.parse(fs.readFileSync(0, "utf8"));
if (!Array.isArray(input.cases)) throw new Error("Explicit cases list required");
const cases = input.cases.map(c => {
  const date = new Date(c.utc);
  if (Number.isNaN(+date) || !c.utc.endsWith("Z")) throw new Error("Require UTC instant");
  const format = new Intl.DateTimeFormat("en-GB", {
    timeZone:c.zone, calendar:"gregory", numberingSystem:"latn",
    year:"numeric", month:"2-digit", day:"2-digit",
    hour:"2-digit", hourCycle:"h23", minute:"2-digit", second:"2-digit",
  });
  const x = Object.fromEntries(format.formatToParts(date).filter(p=>p.type!=="literal").map(p=>[p.type,p.value]));
  return {id:c.id,utc:c.utc,zone:c.zone,
    local_clock:`${x.year}-${x.month}-${x.day}T${x.hour}:${x.minute}:${x.second}`};
});
process.stdout.write(JSON.stringify({
  javascript_engine:"Node.js ECMAScript Intl",
  node_version:process.versions.node,
  icu_version:process.versions.icu,
  node_tzdb_version:process.versions.tz ?? null,
  cases
}));
