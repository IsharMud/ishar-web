import './App.css';
import Navbar from './Navbar';

function App() {
  return (
    <div>
     <Navbar />
     <div className="content">
	<div>
           Ishar is an online text-adventure RPG (commonly called a MUD) set in a
           large, unique world of fantasy and magic.  Players do battle with fearsome
           foes (and sometimes each other) to win great wealth and wrest rare prizes
           from the treasure hoards or bloody corpses of their enemies.
	</div>
	<div>
	  Play the game for free by connecting via
any <a href="/clients/">MUD client</a> to <strong>isharmud.com</strong> port <strong>23</strong> or <strong>9999</strong>.
	</div>
	<div className="under">
	  <div className="quote">
	  Some say that the world was formed from the body of the dying Ishar,
and that his bones became the mountains and his blood ran from his
chest til it collected as the sea.  His flowing hair matted into the
fields we till and his skin mouldered and fell away as soil.
From his sinews and organs sprang the races of dwarves, elves, men, gnomes
and all manner of creatures and plants.  And from his heart sprang the very
gods themselves.
	    <div className="attribution">-- Book of Thurvun, 1730 </div>
	  </div>
	</div>
     </div>
    </div>
  );
}

export default App;
