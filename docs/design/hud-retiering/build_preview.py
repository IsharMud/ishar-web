# Generates static, self-contained mockups of the proposed HUD re-tiering.
# Throwaway design artifact (design sign-off → GitHub issue). Uses the real
# --ac-*/--hud-* tokens and component language from hud.css so it reads as the
# real client, not an approximation.

import pathlib

OUT = pathlib.Path(__file__).parent

CSS = r"""
*{box-sizing:border-box}
:root{
 --ac-accent:#fa7; --ac-accent-2:#ffd7b0;
 --ac-bg:#0c0c0d; --ac-panel:#131316; --ac-elev:#1c1c22;
 --ac-border:#2a2a30; --ac-border-2:#3a3a44;
 --ac-text:#d6d6d7; --ac-dim:#8a8a92;
 --ac-ok:#4cbb17; --ac-info:#4a86cf; --ac-warn:#f80; --ac-danger:#d64b4b;
 --ac-ok-wash:rgba(76,187,23,.12); --ac-info-wash:rgba(74,134,207,.14);
 --ac-warn-wash:rgba(255,136,0,.12); --ac-danger-wash:rgba(214,75,75,.14);
 --ac-accent-wash:rgba(255,170,119,.14);
 --ac-radius:.6rem;
 --hud-hp:var(--ac-danger); --hud-mp:var(--ac-info); --hud-mv:var(--ac-ok);
 --hud-gold:#cdcd00; --hud-tgt:#a0408a; --hud-mm:#a05ad0;
 --hud-group:#3fb6a8; --hud-event:#e8b04b;
}
html,body{margin:0;background:#000;color:var(--ac-text);
 font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:14px}
.ic{width:1em;height:1em;fill:none;stroke:currentColor;stroke-width:1.7;
 stroke-linecap:round;stroke-linejoin:round;display:block}
.ic.fill{fill:currentColor;stroke:none}

/* ---- callouts & legend ---- */
.cbadge{position:absolute;z-index:40;width:20px;height:20px;border-radius:50%;
 background:var(--ac-accent);color:#1a1206;font-weight:800;font-size:.72rem;
 display:flex;align-items:center;justify-content:center;
 box-shadow:0 0 0 2px #000,0 1px 4px rgba(0,0,0,.6)}
.tag-new{display:inline-block;font-size:.56rem;font-weight:800;letter-spacing:.06em;
 text-transform:uppercase;color:var(--ac-accent);border:1px solid var(--ac-accent);
 border-radius:3px;padding:0 3px;vertical-align:middle}
.legend{margin:14px auto 0;max-width:1180px;padding:12px 16px;background:var(--ac-panel);
 border:1px solid var(--ac-border);border-radius:var(--ac-radius)}
.legend h4{margin:0 0 8px;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ac-dim)}
.legend ol{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 24px}
.legend li{font-size:.82rem;line-height:1.35;display:flex;gap:8px;align-items:flex-start}
.legend .n{flex:none;width:18px;height:18px;border-radius:50%;background:var(--ac-accent);
 color:#1a1206;font-weight:800;font-size:.68rem;display:flex;align-items:center;justify-content:center;margin-top:1px}
.legend b{color:var(--ac-accent-2)}
.caption{max-width:1180px;margin:0 auto 10px;color:var(--ac-dim);font-size:.82rem}
.caption b{color:var(--ac-text)}
.frame{padding:16px}

/* ---- app grid ---- */
.app{display:grid;gap:6px;background:#000;position:relative}
.desktop .app{grid-template-columns:232px minmax(0,1fr) 262px;
 grid-template-rows:auto minmax(0,1fr);
 grid-template-areas:"topbar topbar topbar" "left center right";
 height:788px;max-width:1180px;margin:0 auto}
.a-top{grid-area:topbar}.a-left{grid-area:left}.a-center{grid-area:center}.a-right{grid-area:right}

/* ---- topbar ---- */
.topbar{display:flex;align-items:center;gap:12px;background:var(--ac-panel);
 border:1px solid var(--ac-border);border-radius:var(--ac-radius);padding:6px 10px;position:relative}
.status{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--ac-dim);flex:none}
.dot{width:8px;height:8px;border-radius:50%;background:var(--ac-ok);box-shadow:0 0 6px var(--ac-ok)}
.vitals{display:flex;gap:10px;flex:1;align-items:center;min-width:0;flex-wrap:wrap}
.vbar{display:flex;align-items:center;gap:5px;flex:1 1 100px;min-width:96px;max-width:210px}
.vbar-label{font-size:.68rem;font-weight:700;color:var(--ac-dim);width:26px}
.vbar-track{position:relative;flex:1;height:14px;background:var(--ac-bg);
 border:1px solid var(--ac-border);border-radius:7px;overflow:hidden}
.vbar-fill{position:absolute;inset:0 auto 0 0;height:100%;opacity:.85}
.vbar.hp .vbar-fill{background:var(--hud-hp)}.vbar.mp .vbar-fill{background:var(--hud-mp)}
.vbar.mv .vbar-fill{background:var(--hud-mv)}.vbar.mm .vbar-fill{background:var(--hud-mm)}
.vbar.tgt .vbar-fill{background:var(--hud-tgt)}
.vbar-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font-size:.66rem;font-weight:700;color:#fff;text-shadow:0 1px 2px #000;font-variant-numeric:tabular-nums}
.top-actions{display:flex;gap:5px;flex:none}
.iconbtn{width:30px;height:30px;border:1px solid var(--ac-border-2);border-radius:6px;
 background:var(--ac-elev);color:var(--ac-dim);display:flex;align-items:center;justify-content:center}
.iconbtn.accent{color:var(--ac-accent);border-color:rgba(255,170,119,.45)}
.iconbtn .ic{width:16px;height:16px}

/* ---- self-buff ambient row ---- */
.selfbuffs{display:flex;gap:4px;flex:none;align-items:center;padding-left:6px;
 border-left:1px solid var(--ac-border);position:relative;flex-wrap:wrap;max-width:352px}
.sb{width:26px;height:26px;position:relative}
.sb-ic{width:26px;height:26px;border:1px solid var(--ac-border-2);border-radius:5px;
 display:flex;align-items:center;justify-content:center;background:var(--ac-elev)}
.sb-ic .ic{width:15px;height:15px}
.sb.buff .sb-ic{border-color:rgba(76,187,23,.5);color:#7fc99a;background:var(--ac-ok-wash)}
.sb.debuff .sb-ic{border-color:rgba(214,75,75,.6);color:#e6836b;background:var(--ac-danger-wash)}
.sb-t{position:absolute;bottom:-3px;right:-4px;font-size:.52rem;font-weight:800;line-height:1.35;
 background:var(--ac-bg);border:1px solid var(--ac-border);border-radius:3px;padding:0 2px;
 color:var(--hud-event);font-variant-numeric:tabular-nums}
.sb.debuff .sb-t{color:#e6836b;border-color:rgba(214,75,75,.5)}
.sb.alarm .sb-ic{animation:pulse 1.1s ease-in-out infinite;box-shadow:0 0 0 0 rgba(214,75,75,.5)}
.sb-more{width:auto;height:26px;padding:0 6px;border:1px dashed var(--ac-border-2);border-radius:5px;
 display:flex;align-items:center;font-size:.6rem;color:var(--ac-dim);font-weight:700}
@keyframes pulse{50%{box-shadow:0 0 8px 1px rgba(214,75,75,.7)}}

/* ---- panels ---- */
.col{display:flex;flex-direction:column;gap:6px;min-height:0}
.panel{background:var(--ac-panel);border:1px solid var(--ac-border);
 border-radius:var(--ac-radius);position:relative;display:flex;flex-direction:column;min-height:0}
.panel-h{display:flex;align-items:center;gap:6px;padding:6px 8px;border-bottom:1px solid var(--ac-border)}
.panel-h .t{flex:1;font-size:.7rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--ac-dim)}
.panel-h .cnt{font-size:.68rem;color:var(--ac-dim);font-weight:700}
.panel-h .caret{color:var(--ac-dim);font-size:.6rem}
.panel-body{padding:6px 8px;overflow:auto}
.sub-h{font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ac-dim);
 margin:6px 0 3px;font-weight:700}

/* ---- sustain cockpit ---- */
.aff-list{list-style:none;margin:0;padding:0}
.aff{display:flex;align-items:center;gap:7px;font-size:.8rem;padding:4px 6px;
 border-left:3px solid var(--ac-info);border-radius:2px;margin-bottom:3px;background:var(--ac-elev)}
.aff.soon{background:rgba(255,136,0,.10);border-left-color:var(--ac-warn)}
.aff-ic{width:20px;height:20px;flex:none;color:#7fb2e6}
.aff-ic .ic{width:20px;height:20px}
.aff-body{flex:1;min-width:0;display:flex;flex-direction:column;line-height:1.25}
.aff-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.aff-tgt{font-size:.68rem}
.aff-tgt.mate{color:var(--hud-group)}.aff-tgt.foe{color:#c76bb0}.aff-tgt.self{color:var(--ac-dim)}
.aff-time{font-size:.72rem;color:var(--ac-dim);font-variant-numeric:tabular-nums;flex:none}
.aff.soon .aff-time{color:var(--ac-warn);font-weight:700}
.aff-rel{flex:none;font-size:.6rem;color:var(--ac-dim);border:1px solid var(--ac-border-2);
 border-radius:4px;padding:2px 5px;background:var(--ac-panel)}

/* ---- chat ---- */
.chat{flex:1;display:flex;flex-direction:column;min-height:0}
.chat-tabs{display:flex;gap:3px;padding:6px 8px 0}
.chat-tabs button{font-size:.68rem;color:var(--ac-dim);background:none;border:none;
 border-bottom:2px solid transparent;padding:3px 6px}
.chat-tabs button.on{color:var(--ac-accent);border-bottom-color:var(--ac-accent)}
.chat-log{flex:1;overflow:auto;padding:6px 8px;display:flex;flex-direction:column;gap:4px;font-size:.78rem;line-height:1.3}
.chat-log .who{font-weight:700}
.ch-goss{color:var(--ac-accent-2)}.ch-tell{color:#c76bb0}.ch-auc{color:var(--hud-event)}.ch-grp{color:var(--hud-group)}
.chat-in{display:flex;gap:5px;padding:6px 8px;border-top:1px solid var(--ac-border);align-items:center}
.chan-sel{font-size:.7rem;color:var(--ac-accent-2);background:var(--ac-elev);
 border:1px solid var(--ac-border-2);border-radius:5px;padding:4px 6px;white-space:nowrap}
.chat-in input{flex:1;background:var(--ac-bg);border:1px solid var(--ac-border-2);
 border-radius:5px;color:var(--ac-text);padding:5px 7px;font-size:.76rem}

/* ---- group / occupants ---- */
.rowlist{list-style:none;margin:0;padding:0}
.grp{display:flex;gap:6px;padding:4px 6px;border-left:3px solid transparent;border-radius:3px;align-items:flex-start}
.grp:hover{background:var(--ac-elev)}
.grp.tank{border-left-color:var(--hud-hp)}
.grp-main{flex:1;min-width:0}
.grp-line{display:flex;align-items:baseline;gap:5px}
.grp-name{font-size:.8rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.grp-hp{margin-left:auto;font-size:.72rem;font-weight:700;font-variant-numeric:tabular-nums}
.hp-ok{color:var(--ac-ok)}.hp-mid{color:var(--hud-event)}.hp-low{color:var(--hud-hp)}
.grp-bars{display:flex;gap:2px;margin-top:3px}
.mini{width:26px;height:7px;background:var(--ac-bg);border:1px solid var(--ac-border);border-radius:2px;overflow:hidden}
.mini span{display:block;height:100%}
.mini.hp span{background:var(--hud-hp)}.mini.mp span{background:var(--hud-mp)}.mini.mv span{background:var(--hud-mv)}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:3px}
.chip{font-size:.6rem;padding:1px 5px;border:1px solid var(--ac-border-2);border-radius:10px;color:var(--ac-dim)}
.chip.tank{color:var(--hud-hp);border-color:rgba(214,75,75,.5);background:var(--ac-danger-wash);font-weight:700}
.chip.fight{color:var(--ac-text)}
.chip.away{color:var(--ac-dim)}
.occ{display:flex;align-items:center;gap:6px;padding:4px 6px;border-radius:3px;font-size:.8rem}
.occ:hover{background:var(--ac-elev)}
.occ .nm{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.occ .odot{width:7px;height:7px;border-radius:50%;flex:none}
.odot.foe{background:var(--hud-hp)}.odot.friend{background:var(--hud-friendly,var(--ac-ok))}.odot.neut{background:var(--ac-dim)}
.occ .otag{font-size:.58rem;padding:0 4px;border-radius:3px;border:1px solid var(--ac-border-2);color:var(--ac-dim)}
.otag.target{color:#c76bb0;border-color:#7a3a68}

/* ---- minimap ---- */
.mm{height:118px;background:var(--ac-bg);border-radius:4px;position:relative;overflow:hidden;margin:2px}
.mm .room{position:absolute;width:22px;height:16px;border:1px solid var(--ac-border-2);
 background:#26262c;border-radius:2px}
.mm .room.cur{background:var(--ac-accent-wash);border-color:var(--ac-accent);box-shadow:0 0 6px rgba(255,170,119,.5)}
.mm .edge{position:absolute;background:var(--ac-border-2)}

/* ---- collapsible panels + compact (raid) group density ---- */
.panel.collapsed .panel-body,.panel.collapsed .chat-tabs,.panel.collapsed .rose-wrap{display:none}
.panel.collapsed .panel-h{border-bottom:none}
.panel.collapsed .caret{display:inline-block;transform:rotate(-90deg)}
.colcap{font-size:.7rem;letter-spacing:.09em;text-transform:uppercase;color:var(--ac-accent-2);
 margin:0 0 6px;font-weight:700}
.dens{margin-left:6px;font-size:.55rem;color:var(--ac-accent-2);border:1px solid rgba(255,170,119,.4);
 border-radius:4px;padding:0 4px;font-weight:700}
.grp.cmp{display:flex;align-items:center;gap:6px;padding:3px 6px;border-left:3px solid transparent;border-radius:3px}
.grp.cmp:hover{background:var(--ac-elev)}
.grp.cmp.tank{border-left-color:var(--hud-hp)}
.grp.cmp .cn{font-size:.75rem;flex:0 0 58px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.grp.cmp .cbar{flex:1;height:11px;background:var(--ac-bg);border:1px solid var(--ac-border);
 border-radius:5px;overflow:hidden}
.grp.cmp .cbar span{display:block;height:100%}
.grp.cmp .cbar span.hp-ok{background:var(--hud-mv)}
.grp.cmp .cbar span.hp-mid{background:var(--hud-event)}
.grp.cmp .cbar span.hp-low{background:var(--hud-hp)}
.grp.cmp .cp{flex:0 0 30px;text-align:right;font-size:.7rem;font-weight:700;font-variant-numeric:tabular-nums}
.grp.cmp .ct{flex:0 0 auto;font-size:.53rem;color:var(--ac-dim);border:1px solid var(--ac-border-2);
 border-radius:8px;padding:0 4px}
.grp.cmp .ct.tank{color:var(--hud-hp);border-color:rgba(214,75,75,.5);font-weight:700}
.grp.cmp .ct.cc{color:var(--ac-warn);border-color:rgba(255,136,0,.5);font-weight:700}

/* ---- compass rose ---- */
.rose-wrap{display:flex;gap:10px;align-items:center;padding:6px 8px}
.rose{display:grid;grid-template-columns:repeat(3,26px);grid-template-rows:repeat(3,26px);gap:3px}
.rose button{border:1px solid var(--ac-border-2);background:var(--ac-elev);color:var(--ac-accent-2);
 border-radius:5px;font-size:.7rem;font-weight:700}
.rose button.off{color:var(--ac-border-2);border-style:dashed;background:transparent}
.rose .mid{color:var(--ac-dim);font-size:.6rem}
.rose-ud{display:flex;flex-direction:column;gap:3px}
.rose-ud button{width:34px;height:26px;border:1px solid var(--ac-border-2);background:var(--ac-elev);
 color:var(--ac-accent-2);border-radius:5px;font-size:.62rem;font-weight:700}

/* ---- center: terminal / xp / action / input ---- */
.center{display:flex;flex-direction:column;gap:6px;min-height:0}
.term{flex:1;background:#000;border:1px solid var(--ac-border);border-radius:var(--ac-radius);
 padding:8px 10px;font-family:"Courier New",monospace;font-size:13px;line-height:1.4;overflow:hidden;min-height:0}
.term .g{color:#4cbb17}.term .w{color:#c0c0c0}.term .r{color:#ff5555}.term .c{color:#00cdcd}
.term .y{color:#cdcd00}.term .d{color:#8a8a92}.term .m{color:#cd6fcd}.term .b{color:#5599ff}
.xpstrip{position:relative;height:16px;background:var(--ac-bg);border:1px solid var(--ac-border);
 border-radius:8px;overflow:hidden}
.xpstrip .fill{position:absolute;inset:0 auto 0 0;background:var(--hud-gold);opacity:.55}
.xpstrip .lab{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font-size:.62rem;font-weight:700;color:#000;letter-spacing:.05em;text-shadow:0 1px 1px rgba(255,255,255,.25)}
.actionrow{display:flex;gap:8px;align-items:center;position:relative}
.hotbar{display:flex;gap:5px;flex:1;min-width:0;overflow:hidden}
.skill{width:46px;height:46px;flex:none;position:relative;border:1px solid var(--ac-border-2);
 border-bottom-width:3px;border-bottom-color:var(--ac-border-2);border-radius:7px;background:var(--ac-elev);
 display:flex;align-items:center;justify-content:center}
.skill .si{width:30px;height:30px}
.skill.cat-damage{border-bottom-color:var(--ac-danger)}.skill.cat-damage .si{color:#e6836b}
.skill.cat-heal{border-bottom-color:var(--ac-ok)}.skill.cat-heal .si{color:#7fc99a}
.skill.cat-misc{border-bottom-color:var(--ac-info)}.skill.cat-misc .si{color:#7fb2e6}
.skill.item{border-bottom-color:var(--hud-gold)}.skill.item .si{color:#d9c96a}
.skill .key{position:absolute;top:1px;left:3px;font-size:.6rem;font-weight:700;color:var(--ac-dim)}
.skill .count{position:absolute;bottom:1px;right:3px;font-size:.62rem;font-weight:800;color:var(--ac-accent-2);
 text-shadow:0 1px 2px #000}
.skill .cd{position:absolute;inset:0;border-radius:6px;display:flex;align-items:center;justify-content:center;
 font-size:.9rem;font-weight:800;color:#fff;background:conic-gradient(rgba(0,0,0,.72) 0 300deg,transparent 300deg 360deg)}
.skill.empty{border-style:dashed;border-bottom-style:dashed;background:var(--ac-bg);opacity:.5}
.skill.empty .key{top:50%;left:50%;transform:translate(-50%,-50%);font-size:.8rem}
.skill.util{background:var(--ac-panel);border-bottom-color:var(--ac-accent);width:38px}
.skill.util .si{width:18px;height:18px;color:var(--ac-accent);opacity:.85}
.micro{display:flex;gap:5px;flex:none;padding-left:6px;border-left:1px solid var(--ac-border);position:relative}
.mbtn{width:34px;height:34px;border:1px solid var(--ac-border-2);border-radius:6px;background:var(--ac-elev);
 color:var(--ac-dim);display:flex;align-items:center;justify-content:center;position:relative}
.mbtn .ic{width:17px;height:17px}
.mbtn.unread::after{content:"";position:absolute;top:-3px;right:-3px;width:8px;height:8px;
 border-radius:50%;background:var(--ac-accent);box-shadow:0 0 0 2px var(--ac-panel)}
.cmd{display:flex;gap:8px;align-items:center}
.cmd input{flex:1;background:var(--ac-bg);border:1px solid var(--ac-border-2);border-radius:6px;
 color:var(--ac-text);padding:7px 9px;font-family:monospace;font-size:15px}
.sendbtn{border:1px solid rgba(255,170,119,.45);color:var(--ac-accent);background:var(--ac-elev);
 border-radius:6px;padding:7px 12px;font-size:.82rem;font-weight:700;display:flex;gap:6px;align-items:center}
.sendbtn .ic{width:15px;height:15px}

/* ---- phone ---- */
.phone .app{display:flex;flex-direction:column;width:390px;margin:0 auto;
 height:788px;gap:5px;position:relative}
.phone .center{flex:1;min-height:0}
.phone .topbar{flex-wrap:wrap;gap:8px 10px}
.phone .vitals{order:2;flex-basis:100%}
.phone .selfbuffs{order:3;border-left:none;padding-left:0}
.phone .term{font-size:12px}
.dock{display:flex;gap:4px;overflow-x:auto;background:var(--ac-panel);border:1px solid var(--ac-border);
 border-radius:var(--ac-radius);padding:6px;position:relative}
.dbtn{flex:none;width:52px;display:flex;flex-direction:column;align-items:center;gap:2px;
 color:var(--ac-dim);position:relative;padding:2px 0}
.dbtn .ic{width:20px;height:20px}
.dbtn span{font-size:.58rem}
.dbtn.on{color:var(--ac-accent)}
.dbtn.alarm::after{content:"";position:absolute;top:0;right:11px;width:8px;height:8px;border-radius:50%;
 background:var(--hud-hp);box-shadow:0 0 6px var(--hud-hp)}
.sheet{position:absolute;left:0;right:0;bottom:0;background:var(--ac-panel);
 border:1px solid var(--ac-border-2);border-radius:14px 14px 0 0;box-shadow:0 -8px 24px rgba(0,0,0,.6);
 max-height:74%;display:flex;flex-direction:column;z-index:20}
.sheet-h{display:flex;align-items:center;gap:8px;padding:10px 12px;border-bottom:1px solid var(--ac-border)}
.grip{position:absolute;top:6px;left:50%;transform:translateX(-50%);width:36px;height:4px;
 border-radius:2px;background:var(--ac-border-2)}
.sheet-h .t{flex:1;font-size:.86rem;font-weight:700}
.sheet-body{overflow:auto;padding:8px 12px}
.scrim{position:absolute;inset:0;background:rgba(0,0,0,.5);z-index:15}

/* ---- bags ---- */
.bag{border:1px solid var(--ac-border);border-radius:6px;margin-bottom:8px;overflow:hidden}
.bag-h{display:flex;align-items:center;gap:7px;padding:6px 8px;background:var(--ac-elev)}
.bag-h .ic{width:16px;height:16px;color:var(--ac-dim)}
.bag-h .nm{font-size:.8rem;font-weight:700;flex:1}
.bag-h .prov{font-size:.6rem;padding:1px 5px;border-radius:3px;border:1px solid var(--ac-border-2);color:var(--ac-dim)}
.bag-h .prov.worn{color:var(--hud-event);border-color:rgba(232,176,75,.4)}
.bag-h .lock{font-size:.66rem;color:var(--ac-warn)}
.bag-items{list-style:none;margin:0;padding:4px 8px}
.bag-items li{display:flex;font-size:.78rem;padding:2px 0;color:var(--ac-text)}
.bag-items li .qty{margin-left:auto;color:var(--ac-dim);font-variant-numeric:tabular-nums}
.bag-items li.dim{color:var(--ac-dim);font-style:italic}
.pin{margin-left:8px;font-size:.58rem;color:var(--ac-accent);border:1px solid rgba(255,170,119,.4);
 border-radius:3px;padding:0 4px}
"""

SPRITE = """
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
 <symbol id="i-fire" viewBox="0 0 24 24"><path class="p" d="M12 2c2 4-1 5.5 .5 8 .8-.7 1.2-1.8 1.2-3 2 1.7 3.3 4.2 3.3 7a5 5 0 1 1-10 0c0-1.6.7-2.8 1.6-3.8-.1 1 .4 1.9 1.1 2.3-.6-2.9 1.3-4.6 1.3-10.5z"/></symbol>
 <symbol id="i-frost" viewBox="0 0 24 24"><g><path d="M12 2v20M3.3 7l17.4 10M20.7 7L3.3 17"/><path d="M12 6l-2 2M12 6l2 2M12 18l-2-2M12 18l2-2"/></g></symbol>
 <symbol id="i-heal" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
 <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l7 3v5c0 4.2-3 7.5-7 9-4-1.5-7-4.8-7-9V6z"/></symbol>
 <symbol id="i-star" viewBox="0 0 24 24"><path class="p" d="M12 3l1.8 5.4L19 10l-4.5 2.2L13 18l-1-4-1 4-1.5-5.8L5 10l5.2-1.6z"/></symbol>
 <symbol id="i-bolt" viewBox="0 0 24 24"><path class="p" d="M13 2L5 13h5l-1 9 9-12h-6z"/></symbol>
 <symbol id="i-flask" viewBox="0 0 24 24"><path d="M10 3h4M10.5 3v6L5.5 18a2 2 0 0 0 1.8 3h9.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 14h9"/></symbol>
 <symbol id="i-scroll" viewBox="0 0 24 24"><path d="M6 5a2 2 0 0 1 2 2v10a2 2 0 0 0 2 2h8a2 2 0 0 1-2-2V7a2 2 0 0 0-2-2z"/><path d="M10 9h6M10 12h6"/></symbol>
 <symbol id="i-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/></symbol>
 <symbol id="i-map" viewBox="0 0 24 24"><path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/></symbol>
 <symbol id="i-armor" viewBox="0 0 24 24"><path d="M6 4l6 2 6-2 1 5-3 1v9H8v-9L5 9z"/></symbol>
 <symbol id="i-bag" viewBox="0 0 24 24"><path d="M6 8h12l1 12H5zM9 8V6a3 3 0 0 1 6 0v2"/></symbol>
 <symbol id="i-person" viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.4"/><path d="M5.5 20a6.5 6.5 0 0 1 13 0"/></symbol>
 <symbol id="i-people" viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"/><path d="M3.5 19a5.5 5.5 0 0 1 11 0"/><path d="M16 6.2A3 3 0 0 1 18 12M16.5 14.5A5.5 5.5 0 0 1 20.5 19"/></symbol>
 <symbol id="i-chat" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></symbol>
 <symbol id="i-search" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/></symbol>
 <symbol id="i-send" viewBox="0 0 24 24"><path class="p" d="M3 11l18-8-8 18-2-7z"/></symbol>
 <symbol id="i-sidebar" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/></symbol>
 <symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="2.5"/></symbol>
 <symbol id="i-spark" viewBox="0 0 24 24"><path class="p" d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5zM18 14l.8 2.2L21 17l-2.2.8L18 20l-.8-2.2L15 17l2.2-.8z"/></symbol>
</svg>
"""

def ic(name, cls="ic", fill=False):
    c = cls + (" fill" if fill else "")
    return f'<svg class="{c}" viewBox="0 0 24 24"><use href="#i-{name}"/></svg>'

# game-icons use filled paths for some glyphs; mark those symbols' .p children fill
FILLED = {"fire", "star", "bolt", "send", "spark"}
def si(name):
    fill = name in FILLED
    return ic(name, cls="si ic", fill=fill)

def slot(key, name, cat, icon, count=None, cd=None, empty=False, badge=None):
    if empty:
        return f'<div class="skill empty"><span class="key">{key}</span></div>'
    cls = "skill item" if cat == "item" else f"skill cat-{cat}"
    fillc = " fill" if icon in FILLED else ""
    parts = [f'<span class="key">{key}</span>',
             f'<svg class="si ic{fillc}" viewBox="0 0 24 24"><use href="#i-{icon}"/></svg>']
    if count is not None:
        parts.append(f'<span class="count">&times;{count}</span>')
    if cd is not None:
        parts.append(f'<span class="cd">{cd}</span>')
    if badge is not None:
        parts.append(f'<span class="cbadge" style="top:-9px;left:-9px">{badge}</span>')
    return f'<div class="{cls}">{"".join(parts)}</div>'

def sustain(name, icon, tgt, tcls, time, soon=False):
    return (f'<li class="aff{" soon" if soon else ""}">'
            f'<span class="aff-ic">{ic(icon)}</span>'
            f'<span class="aff-body"><span class="aff-name">{name}</span>'
            f'<span class="aff-tgt {tcls}">&rsaquo; {tgt}</span></span>'
            f'<span class="aff-time">{time}</span>'
            f'<span class="aff-rel">release</span></li>')

# --- shared fragments ---
# A self-affect icon. Bare by rule: a timer chip appears (and the tile pulses)
# only when it's about to drop, so a quest group's ~10 buffs stay a compact row.
def sb(icon, kind="buff", timer=None, soon=False):
    glyph = ic(icon, "ic", icon in FILLED)
    cls = "sb " + kind + (" alarm" if soon else "")
    t = f'<span class="sb-t">{timer}</span>' if timer else ''
    return f'<div class="{cls}"><div class="sb-ic">{glyph}</div>{t}</div>'

# 9 buffs (mostly long quest buffs, bare) + a short buff and a debuff that show a
# pulsing countdown — the "about to drop" signal that draws the eye.
SB_ITEMS = "".join([sb("shield"), sb("bolt"), sb("star"), sb("heal"), sb("eye"),
            sb("spark"), sb("shield"), sb("bolt"),
            sb("star", "buff", "0:52", True), sb("frost", "debuff", "0:45", True)])

def selfbuffs(badge=True, plain=False):
    b = '<span class="cbadge" style="top:-9px;left:-9px">1</span>' if badge else ''
    style = ' style="border-left:none;padding-left:0;max-width:none"' if plain else ''
    return f'<div class="selfbuffs"{style}>{b}{SB_ITEMS}</div>'

VITALS = '''<div class="vitals">
  <div class="vbar hp"><span class="vbar-label">HP</span><span class="vbar-track"><span class="vbar-fill" style="width:86%"></span><span class="vbar-text">412 / 480</span></span></div>
  <div class="vbar mp"><span class="vbar-label">MP</span><span class="vbar-track"><span class="vbar-fill" style="width:43%"></span><span class="vbar-text">130 / 300</span></span></div>
  <div class="vbar mv"><span class="vbar-label">MV</span><span class="vbar-track"><span class="vbar-fill" style="width:82%"></span><span class="vbar-text">198 / 240</span></span></div>
  <div class="vbar tgt"><span class="vbar-label">TGT</span><span class="vbar-track"><span class="vbar-fill" style="width:35%"></span><span class="vbar-text">35%</span></span></div>
</div>'''

TOP_ACTIONS = f'''<div class="top-actions">
  <div class="iconbtn">{ic("search")}</div>
  <div class="iconbtn">{ic("gear")}</div>
  <div class="iconbtn">{ic("sidebar")}</div>
  <div class="iconbtn accent">{ic("sidebar")}</div>
</div>'''

TERM = '''<div class="term">
<div class="g">The Grand Concourse</div>
<div class="w">A vast marble hall stretches beneath a vaulted ceiling, banners of the</div>
<div class="w">old kingdoms hanging in the still air. Exits lead in all directions.</div>
<div class="d">&nbsp;</div>
<div><span class="w">A towering city guard stands watch here.</span></div>
<div><span class="r">A scarred alley thug</span> <span class="w">is here, snarling at Boric.</span></div>
<div><span class="c">Hadeon the curio merchant</span> <span class="w">tends his stall.</span></div>
<div class="d">&nbsp;</div>
<div><span class="r">Your fireball</span> <span class="w">scorches</span> <span class="r">a scarred alley thug!</span></div>
<div><span class="w">A wiry crossroads bandit</span> <span class="r">claws you</span> <span class="w">for 14 damage.</span></div>
<div class="m">Boric gossips: 'anyone up for the crypt run?'</div>
<div class="d">&gt; cast fireball thug</div>
</div>'''

def action_block(callouts=True, micro=True):
    xp_badge = '<span class="cbadge" style="top:-9px;left:8px">2</span>' if callouts else ''
    micro_badge = '<span class="cbadge" style="top:-9px;left:-8px">6</span>' if callouts else ''
    slots = "".join([
        slot("1","Fireball","damage","fire"),
        slot("2","Frost Bolt","damage","frost"),
        slot("3","Heal","heal","heal",cd="8"),
        slot("4","Stoneskin","misc","shield"),
        slot("5","Healing Potion","item","flask",count=3,badge=("3" if callouts else None)),
        slot("6","Scroll of Recall","item","scroll",count=2),
        slot("7","Magic Missile","damage","star"),
        slot("8","","damage","",empty=True),
    ])
    util = f'<div class="skill util">{si("gear")}</div>'
    micro_html = f'''<div class="micro">{micro_badge}
      <div class="mbtn unread">{ic("gear")}</div>
      <div class="mbtn">{ic("map")}</div>
      <div class="mbtn">{ic("armor")}</div>
      <div class="mbtn">{ic("bag")}</div>
      <div class="mbtn">{ic("person")}</div>
      <div class="mbtn">{ic("spark")}</div>
      <div class="mbtn">{ic("people")}</div>
    </div>''' if micro else ''
    return f'''
    <div class="xpstrip">{xp_badge}<span class="fill" style="width:62%"></span>
      <span class="lab">XP &mdash; 62% to level 46</span></div>
    <div class="actionrow"><div class="hotbar">{slots}</div>{util}{micro_html}</div>'''

SUSTAIN = f'''<section class="panel" style="flex:none">
  <span class="cbadge" style="top:-9px;left:-9px">4</span>
  <div class="panel-h"><span class="t">Tracked Spells</span><span class="cnt">5</span><span class="caret">&#9662;</span></div>
  <div class="panel-body">
   <ul class="aff-list">
    {sustain("Faerie Fire","spark","a scarred alley thug","foe","1:10",soon=True)}
    {sustain("Haste","bolt","Kael","mate","3:20")}
    {sustain("Detect Invis","eye","self","self","10:00")}
    {sustain("Bless","star","self","self","12:40")}
    {sustain("Shroud","shield","Boric","mate","15:00")}
   </ul>
  </div>
</section>'''

CHAT = f'''<section class="panel chat">
  <span class="cbadge" style="top:-9px;left:-9px">5</span>
  <div class="chat-tabs"><button class="on">All</button><button>Gossip</button><button>Tells</button><button>Group</button></div>
  <div class="chat-log">
    <div><span class="who ch-goss">Boric</span> <span class="d">gossips:</span> anyone up for the crypt run?</div>
    <div><span class="who ch-tell">Selra</span> <span class="d">tells you:</span> omw, 2 rooms out</div>
    <div><span class="who ch-auc">Hadeon</span> <span class="d">auctions:</span> WTS dragonscale helm, 50k</div>
    <div><span class="who ch-grp">Kael</span> <span class="d">(group):</span> pulling in 5</div>
    <div><span class="who ch-goss">Mirena</span> <span class="d">gossips:</span> grats on the level!</div>
  </div>
  <div class="chat-in"><span class="chan-sel">Gossip &#9662;</span><input placeholder="message #gossip&hellip;"></div>
</section>'''

def group_panel():
    def row(name, hp, hpcls, bars, chips="", tank=False):
        b = "".join(f'<span class="mini {k}"><span style="width:{v}%"></span></span>' for k,v in bars)
        return (f'<li class="grp{" tank" if tank else ""}"><div class="grp-main">'
                f'<div class="grp-line"><span class="grp-name">{name}</span>'
                f'<span class="grp-hp {hpcls}">{hp}</span></div>'
                f'<div class="grp-bars">{b}</div>{chips}</div></li>')
    rows = "".join([
        row("Aelwyn <span class='d'>&#9733;</span>","86%","hp-ok",[("hp",86),("mp",43),("mv",82)]),
        row("Boric","30%","hp-low",[("hp",30),("mp",40),("mv",75)],
            '<div class="chips"><span class="chip tank">TANK</span><span class="chip fight">&#9876; thug</span></div>',tank=True),
        row("Selra","95%","hp-ok",[("hp",95),("mp",90),("mv",88)],
            '<div class="chips"><span class="chip away">Cramped Alcove</span></div>'),
        row("Kael","72%","hp-mid",[("hp",72),("mp",60),("mv",80)],
            '<div class="chips"><span class="chip away">Village Sq.</span></div>'),
    ])
    return f'''<section class="panel">
      <div class="panel-h"><span class="t">Group</span><span class="cnt">5</span><span class="caret">&#9662;</span></div>
      <div class="panel-body"><ul class="rowlist">{rows}</ul></div></section>'''

def occ_panel():
    def row(dot,name,tags):
        t = "".join(f'<span class="otag {c}">{x}</span>' for x,c in tags)
        return f'<li class="occ"><span class="odot {dot}"></span><span class="nm">{name}</span>{t}</li>'
    rows="".join([
        row("foe","a scarred alley thug",[("hostile",""),("target","target")]),
        row("foe","a wiry crossroads bandit",[("fights you","")]),
        row("neut","a towering city guard",[]),
        row("neut","Hadeon the curio merchant",[("shop","")]),
        row("friend","a large timber wolf",[("yours","")]),
    ])
    return f'''<section class="panel">
      <div class="panel-h"><span class="t">Here</span><span class="cnt">6</span><span class="caret">&#9662;</span></div>
      <div class="panel-body"><ul class="rowlist">{rows}</ul></div></section>'''

def collapsed_panel(title, cnt=""):
    c = f'<span class="cnt">{cnt}</span>' if cnt else ''
    return (f'<section class="panel collapsed" style="flex:none"><div class="panel-h">'
            f'<span class="t">{title}</span>{c}<span class="caret">&#9662;</span></div></section>')

# The raid-density group: one line per member (name · HP bar · %), so a full
# group + allies fits and the panel scrolls past what doesn't.
def compact_group(title="Group", cnt="8"):
    mem=[("Aelwyn &#9733;","86","hp-ok",""),("Boric","30","hp-low","tank"),("Selra","95","hp-ok","slp"),
         ("Kael","72","hp-mid","away"),("Mirena","100","hp-ok",""),("Doran","54","hp-mid","stun"),
         ("Ysolde","41","hp-mid","away"),("Thane","88","hp-ok","")]
    allies=[("a timber wolf","60","hp-mid",""),("a fire elemental","100","hp-ok","")]
    CHIP={"tank":("tank","TANK"),"away":("away","away"),"slp":("cc","asleep"),
          "stun":("cc","stunned"),"flee":("cc","fleeing")}
    def row(nm,hp,cls,tag):
        cc,label = CHIP.get(tag,("",""))
        t = f'<span class="ct {cc}">{label}</span>' if cc else ''
        return (f'<li class="grp cmp{" tank" if tag=="tank" else ""}"><span class="cn">{nm}</span>'
                f'<span class="cbar"><span class="{cls}" style="width:{hp}%"></span></span>'
                f'<span class="cp {cls}">{hp}%</span>{t}</li>')
    rows="".join(row(*m) for m in mem)
    arows="".join(row(*a) for a in allies)
    return (f'<section class="panel"><div class="panel-h"><span class="t">{title}</span>'
            f'<span class="cnt">{cnt}</span><span class="dens">compact</span>'
            f'<span class="caret">&#9662;</span></div>'
            f'<div class="panel-body"><ul class="rowlist">{rows}</ul>'
            f'<div class="sub-h">Allies</div><ul class="rowlist">{arows}</ul></div></section>')

ROSE_BODY = '''<div class="rose-wrap">
   <div class="rose">
     <button class="off">NW</button><button>N</button><button class="off">NE</button>
     <button>W</button><button class="mid">&#9673;</button><button>E</button>
     <button class="off">SW</button><button>S</button><button class="off">SE</button>
   </div>
   <div class="rose-ud"><button>U</button><button>D</button><button>in</button></div>
  </div>'''

# Room panel keeps the existing Rose | Map tab pair (one panel, zero new real
# estate) rather than promoting the minimap to its own column panel.
ROOM_TABS = f'''<section class="panel" style="flex:none">
  <div class="panel-h"><span class="t">Room &mdash; The Grand Concourse</span></div>
  <div class="chat-tabs" style="padding:6px 8px 2px"><button class="on">Rose</button><button>Map</button></div>
  {ROSE_BODY}
</section>'''

def page(cls, inner, extra_legend):
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body class="{cls}">{SPRITE}<div class="frame">{inner}{extra_legend}</div></body></html>'''

# ---------------- DESKTOP ----------------
desktop_app = f'''
<div class="caption"><b>Ishar HUD — proposed re-tiering</b> · design mock, not the live client · numbered markers = new / moved surfaces</div>
<div class="app">
  <div class="a-top topbar">
    <div class="status"><span class="dot"></span>Connected</div>
    {VITALS}
    {selfbuffs()}
    {TOP_ACTIONS}
  </div>
  <div class="a-left col">
    {group_panel()}
    {occ_panel()}
    {ROOM_TABS}
  </div>
  <div class="a-center center">
    {TERM}
    {action_block()}
    <div class="cmd"><input value="cast fireball thug"><div class="sendbtn">{ic("send","ic fill")}Send</div></div>
  </div>
  <div class="a-right col">
    {SUSTAIN}
    {CHAT}
  </div>
</div>'''

desktop_legend = '''<div class="legend"><h4>What changed</h4><ol>
<li><span class="n">1</span><span><b>Self buffs/debuffs</b> — ambient icons by the vitals (lifted out of the buried Status tab). Bare by default; a timer appears and the tile pulses only when one's about to drop — so a quest group's ~10 buffs stay a compact row (it wraps if the row fills).</span></li>
<li><span class="n">2</span><span><b>XP</b> — thin ambient strip on the action row (moved off the Character panel, which becomes an overlay).</span></li>
<li><span class="n">3</span><span><b>Action bar</b> — now pins consumables: item slots (gold edge) with live counts, alongside skills.</span></li>
<li><span class="n">4</span><span><b>Tracked Spells</b> — the magic you're maintaining: spell · target · timer · release, expiry-sorted (enemy debuff at top, about to drop). Was buried in the Status tab.</span></li>
<li><span class="n">5</span><span><b>Chat</b> — persistent + filtered, with a channel-targeted input (its reason to exist vs. the terminal).</span></li>
<li><span class="n">6</span><span><b>Micro-menu</b> — Equipment / Bags / Character / Abilities / Who open here as overlays; the right-column tab bar is gone.</span></li>
</ol><p style="margin:8px 0 0;font-size:.78rem;color:var(--ac-dim)">Left column keeps the existing <b style="color:var(--ac-accent-2)">Room</b> panel with its <b style="color:var(--ac-accent-2)">Rose | Map</b> tab pair (no standalone minimap).</p></div>'''

(OUT/"preview-desktop.html").write_text(page("desktop", desktop_app, desktop_legend))

# ---------------- PHONE: terminal-first ----------------
def dock(callout=False):
    items=[("compass","Room","i-map",False,False),("people","Here","i-people",False,False),
           ("group","Group","i-person",False,False),("bags","Bags","i-bag",False,False),
           ("gear","Gear","i-armor",False,False),("skills","Skills","i-spark",False,False),
           ("sust","Tracked","i-shield",False,True),("chat","Chat","i-chat",False,False),
           ("char","Char","i-person",False,False),("who","Who","i-eye",False,False)]
    b=""
    for _,lab,sym,on,alarm in items:
        cls="dbtn"+(" on" if on else "")+(" alarm" if alarm else "")
        b+=f'<div class="{cls}"><svg class="ic" viewBox="0 0 24 24"><use href="#{sym}"/></svg><span>{lab}</span></div>'
    badge='<span class="cbadge" style="top:-9px;left:-9px">2</span>' if callout else ''
    return f'<div class="dock">{badge}{b}</div>'

phone_app = f'''
<div class="caption"><b>Phone — terminal-first.</b> No room for columns: ambient stays on top, everything else collapses to the dock.</div>
<div class="app">
  <div class="a-top topbar">
    <div class="status"><span class="dot"></span>Connected</div>
    {TOP_ACTIONS}
    {VITALS}
    {selfbuffs(badge=True, plain=True)}
  </div>
  <div class="a-center center">
    {TERM}
    {action_block(callouts=False, micro=False)}
    <div class="cmd"><input value="cast fireball thug"><div class="sendbtn">{ic("send","ic fill")}</div></div>
  </div>
  {dock(callout=True)}
</div>'''

phone_legend = '''<div class="legend"><h4>Phone notes</h4><ol style="grid-template-columns:1fr">
<li><span class="n">1</span><span><b>Ambient row</b> survives on phone: vitals, self-buff icons, XP strip and the action bar (with pinnable item slots) — the only things worth permanent space on a small screen.</span></li>
<li><span class="n">2</span><span><b>Dock</b> holds everything else, one tap to a bottom sheet. The red dot on <b>Sustain</b> is the ambient alarm — a maintained spell about to drop — so you know to open it without it living on-screen.</span></li>
</ol></div>'''

(OUT/"preview-phone.html").write_text(page("phone", phone_app, phone_legend))

# ---------------- PHONE: bags sheet (aggregated worn + carried) ----------------
def bag(name, prov, provcls, items, locked=False):
    head=f'<div class="bag-h"><svg class="ic" viewBox="0 0 24 24"><use href="#i-bag"/></svg><span class="nm">{name}</span><span class="prov {provcls}">{prov}</span>'
    head+=('<span class="lock">&#128274; locked</span>' if locked else '')+'</div>'
    if locked:
        body='<ul class="bag-items"><li class="dim">locked &mdash; unlock to view contents</li></ul>'
    else:
        pin_span='<span class="pin">pin</span>'
        li="".join(f'<li>{n}{pin_span if pin else ""}<span class="qty">{q}</span></li>' for n,q,pin in items)
        body=f'<ul class="bag-items">{li}</ul>'
    return f'<div class="bag">{head}{body}</div>'

bags_sheet = f'''
<div class="caption"><b>Phone — Bags sheet.</b> The inventory overlay aggregates <b>worn and carried</b> storage together.</div>
<div class="app">
  <div class="a-top topbar"><div class="status"><span class="dot"></span>Connected</div>{VITALS}</div>
  <div class="a-center center">{TERM}{action_block(callouts=False, micro=False)}
    <div class="cmd"><input value=""><div class="sendbtn">{ic("send","ic fill")}</div></div></div>
  {dock(callout=False)}
  <div class="scrim"></div>
  <div class="sheet">
    <span class="grip"></span>
    <span class="cbadge" style="top:-9px;left:14px">3</span>
    <div class="sheet-h"><svg class="ic" viewBox="0 0 24 24" style="width:18px;height:18px"><use href="#i-bag"/></svg>
      <span class="t">Bags</span><span class="prov" style="font-size:.6rem;color:var(--ac-dim)">worn + carried</span></div>
    <div class="sheet-body">
      {bag("a sturdy traveling pack","worn: Back","worn",[("a flask of lamp oil","&times;2",False),("a coil of silk rope","",False),("a glyph of teleportation","&times;2",True)])}
      {bag("a rune-locked coffer","worn: Held","worn",[],locked=True)}
      {bag("a leather sack","carried","",[("a brass key","",False)])}
      <div class="sub-h">Loose in inventory</div>
      <ul class="bag-items" style="padding:0">
        <li><span style="color:#7fb2e6">a glowing potion</span><span class="pin">pin</span><span class="qty">&times;3</span></li>
        <li>a scroll of recall<span class="pin">pin</span><span class="qty">&times;2</span></li>
        <li>a quilted woolen hood<span class="qty"></span></li>
        <li>a tarnished silver band<span class="qty"></span></li>
      </ul>
    </div>
  </div>
</div>'''

bags_legend = '''<div class="legend"><h4>Bags sheet</h4><ol style="grid-template-columns:1fr">
<li><span class="n">3</span><span><b>Aggregated containers.</b> Worn bags (the back pack, the held coffer) show alongside carried ones, tagged by where they live; a locked worn container stays locked. Loose consumables offer a <b>pin</b> action straight to the action bar.</span></li>
</ol></div>'''

(OUT/"preview-bags.html").write_text(page("phone", bags_sheet, bags_legend))

# ---------------- COLUMNS: flexibility (same column, two players) ----------------
columns_app = f'''
<div class="caption"><b>The same left column, two players.</b> Panels stay collapsible and the
group has a compact density &mdash; so the column flexes to whoever's using it, instead of handing
out fixed space.</div>
<div style="display:flex;gap:28px;justify-content:center;align-items:flex-start">
  <div style="width:242px">
    <div class="colcap">Solo / DPS</div>
    <div class="col">{collapsed_panel("Group")}{occ_panel()}{ROOM_TABS}</div>
  </div>
  <div style="width:242px">
    <div class="colcap">Healer &middot; full group + allies</div>
    <div class="col">{compact_group()}{collapsed_panel("Here","6")}{collapsed_panel("Room")}</div>
  </div>
</div>'''

columns_legend = '''<div class="legend"><h4>Flexibility, not fixed space</h4><ol style="grid-template-columns:1fr">
<li><span class="n">A</span><span>Every panel stays <b>collapsible</b> (the caret). A solo player collapses Group; a healer collapses Here and Room so the group owns the column. The topbar's column toggles still hide a whole side.</span></li>
<li><span class="n">B</span><span>Group has two <b>densities</b> you toggle (the <b>compact</b> chip), each opinionated &mdash; not a field-picker. Compact = HP bar &middot; % &middot; one status marker (<b style="color:var(--hud-hp)">tank</b>, <b style="color:var(--ac-warn)">asleep / stunned</b>) &middot; range, so a full group + allies fits. Full mode adds the MP/MV triple. Actions live in each row's tap menu.</span></li>
</ol></div>'''

(OUT/"preview-columns.html").write_text(page("desktop", columns_app, columns_legend))

print("wrote preview-desktop.html, preview-phone.html, preview-bags.html, preview-columns.html")
