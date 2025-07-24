var state = ["runner slight-hitting", "runner medium-hitting", "runner strong-hitting", "runner low-kicking", "runner high-kicking", "runner jumping running", "runner running", "runner standing", "runner crossing-arms", "runner bowing", "runner ready-fighting", "runner blocking", "runner dodging"];
var cc = 0;

function Movement()
{
    document.getElementById("stickman").className = state[cc];
    cc = (cc + 1) % state.length;
}