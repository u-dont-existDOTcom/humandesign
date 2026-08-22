# Ra Uru Hu — Partnership Analysis (IHDS, 2005)

## Status

Primary-source summary for the relationship module.

Source: **Ra Uru Hu, Partnership Analysis**, International Human Design School, 2005, four-part analyst certification training.

This file records source-derived mechanics used by code. It is not a compatibility model and does not claim scientific validation.

## Source-derived implementation rules

### Surface priority

Ra repeatedly instructs analysts to begin with the relationship surface rather than immediately mining deeper substructure.

The code therefore prioritizes:

1. each individual's natal Type/Authority/Profile/Definition;
2. combined Center configuration;
3. split topology in the connection chart;
4. channel connection modes;
5. Type/Profile communication context;
6. Sun/Earth and Nodes as higher-level context.

### Center-count keynotes

The course gives the following shorthand:

- 9 defined / 0 open: `Nowhere to go`;
- 8 defined / 1 open: `Have some fun`;
- 7 defined / 2 open: `Work to do`;
- 6 defined / 3 open: `Better to be free`;
- 5 defined / 4 open: `Not a relationship anymore`.

These are retained as categorical labels only.

### Four connection modes

The course's four basic connection categories are:

- **Electromagnetic** — the partners carry opposite hanging Gates and together complete the Channel;
- **Dominance** — one partner carries the complete Channel and the other carries neither Gate;
- **Compromise** — one partner carries the complete Channel while the other already carries one Gate of it;
- **Companionship** — both independently carry the complete Channel.

The course also notes companionship value in shared Gates. Shared Gates are therefore preserved separately rather than promoted into extra complete Channels.

### Electromagnetic is not compatibility

Ra explicitly warns against treating a high count of Electromagnetics as proof of a good relationship. He describes Electromagnetic connection as genetic attraction/spark that can later become irritating or alienating.

Accordingly the software does not score Electromagnetics as universally positive.

### Compromise direction matters

For Compromise, preserve which person owns the whole Channel and which person contributes only one Gate. The source treats this asymmetry as mechanically important.

### Composite splits matter

The connection chart can itself be split/triple-split. The module preserves exact composite Definition topology rather than collapsing the pair to a Center count alone.

### Nodes / Sun-Earth

Ra uses Nodal lines and Sun/Earth relationships as higher-level relationship context after the surface mechanics. A Sun/Earth placement on another person's Nodes can indicate that the person belongs in the other's landscape, but Ra explicitly says this does not by itself mean lover, spouse, friend, or ideal partner.

The V1 code therefore detects the mechanical alignment without adding soulmate interpretation.

### No source-derived soulmate score

The course does not provide a general numeric compatibility probability or a rule for ranking all possible romantic partners. It focuses on analyzing the mechanics of a relationship that exists or is being considered.

The software must not invent such a scalar and attribute it to Ra.

### Third-party privacy

Ra states discomfort with revealing extensive information about an absent partner to only one member of a couple. The research module keeps this as an output-policy constraint: pair mechanics are calculable, but absent-partner psychological claims should be limited and clearly qualified.

## Future source work

Before implementing deeper relationship layers, freeze exact source rules for:

- Nodal line harmony/resonance;
- Profile harmony in connection;
- relationship-level Authority conventions;
- deeper Gate/Line fixing effects;
- cycle-chart interaction with partnerships.

Do not infer these ad hoc from known couples.
