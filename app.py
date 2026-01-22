 { useState } from 'react';
import { AlertCircle, CheckCircle, Info, Download, Calculator, Thermometer, Package, Settings } from 'lucide-react';

const RefrigerationCalculator = () => {
  const [length, setLength] = useState(3.0);
  const [width, setWidth] = useState(2.0);
  const [height, setHeight] = useState(2.5);
  const [insulation, setInsulation] = useState(100);
  const [tempAmbient, setTempAmbient] = useState(35);
  const [tempInternal, setTempInternal] = useState(0);
  const [productLoad, setProductLoad] = useState(500);
  const [productTemp, setProductTemp] = useState(25);
  const [productType, setProductType] = useState('meat');
  const [tEvap, setTEvap] = useState(-8);
  const [tCond, setTCond] = useState(45);
  const [refrigerant, setRefrigerant] = useState('R404A');
  const [runHours, setRunHours] = useState(18);
  const [showDetails, setShowDetails] = useState(false);

  const productData = {
    meat: { name: 'ხორცი', cp: 3.14, freezingPoint: -2 },
    fish: { name: 'თევზი', cp: 3.78, freezingPoint: -2 },
    dairy: { name: 'რძის ნაწარმი', cp: 3.85, freezingPoint: -1 },
    vegetables: { name: 'ბოსტნეული', cp: 3.98, freezingPoint: -1 },
    fruits: { name: 'ხილი', cp: 3.60, freezingPoint: -2 },
    frozen: { name: 'გაყინული', cp: 2.05, freezingPoint: -18 }
  };

  const uValues = {
    60: 0.367,
    80: 0.275,
    100: 0.220,
    120: 0.183,
    150: 0.147,
    200: 0.110
  };

  const compressorCatalog = [
    { model: "2KES-05Y", capLow: 0.5, capMed: 0.9, power: 0.4, price: 450 },
    { model: "2JES-07Y", capLow: 0.8, capMed: 1.5, power: 0.6, price: 520 },
    { model: "2HES-2Y", capLow: 1.5, capMed: 2.8, power: 1.2, price: 680 },
    { model: "4FES-3Y", capLow: 2.2, capMed: 4.5, power: 2.0, price: 950 },
    { model: "4EES-4Y", capLow: 3.5, capMed: 6.8, power: 3.0, price: 1200 },
    { model: "4DES-5Y", capLow: 4.8, capMed: 9.5, power: 4.5, price: 1450 },
    { model: "4CES-6Y", capLow: 6.5, capMed: 12.0, power: 6.0, price: 1700 },
    { model: "4TES-9Y", capLow: 8.5, capMed: 16.0, power: 8.0, price: 2100 },
    { model: "4PES-12Y", capLow: 10.5, capMed: 20.0, power: 10.5, price: 2400 }
  ];

  const evaporators = [
    { model: "ECO-3", capacity: 1.5, price: 280 },
    { model: "ECO-5", capacity: 3.0, price: 380 },
    { model: "ECO-8", capacity: 5.0, price: 480 },
    { model: "ECO-12", capacity: 8.0, price: 650 },
    { model: "ECO-18", capacity: 12.0, price: 850 },
    { model: "ECO-25", capacity: 18.0, price: 1100 }
  ];

  const calculate = () => {
    const volume = length * width * height;
    const surfaceArea = 2 * (length * width + length * height + width * height);
    const uValue = uValues[insulation];
    const deltaT = tempAmbient - tempInternal;
    const qTransmission = (uValue * surfaceArea * deltaT) / 1000;
    const selectedProduct = productData[productType];
    const cpValue = selectedProduct.cp;
    const qProduct = (productLoad * cpValue * (productTemp - tempInternal)) / (3600 * 1000);
    const qLighting = (5 * volume) / 1000;
    const qPeople = 0.3;
    const qDoorOpenings = qTransmission * 0.10;
    const qAdditional = qLighting + qPeople + qDoorOpenings;
    let safetyFactor = 1.15;
    if (tempInternal < -15) safetyFactor = 1.25;
    if (tempInternal < -25) safetyFactor = 1.30;
    const totalLoadContinuous = (qTransmission + qProduct + qAdditional) * safetyFactor;
    const requiredCapacity = (totalLoadContinuous * 24) / runHours;
    const mode = tEvap < -15 ? 'capLow' : 'capMed';
    let selectedCompressor = null;
    for (let comp of compressorCatalog) {
      if (comp[mode] >= requiredCapacity) {
        selectedCompressor = comp;
        break;
      }
    }
    let selectedEvaporator = null;
    for (let evap of evaporators) {
      if (evap.capacity >= requiredCapacity) {
        selectedEvaporator = evap;
        break;
      }
    }
    return { volume, surfaceArea, qTransmission, qProduct, qAdditional, totalLoadContinuous, requiredCapacity, selectedCompressor, selectedEvaporator, mode, uValue, deltaT, safetyFactor };
  };

  const results = calculate();

  const getWarnings = () => {
    const warnings = [];
    if (tempInternal >= tempAmbient) warnings.push("⚠️ შიდა ტემპერატურა არ შეიძლება იყოს გარე ტემპერატურაზე მეტი!");
    if (productTemp < tempInternal) warnings.push("⚠️ პროდუქტის ტემპერატურა არ შეიძლება იყოს კამერის ტემპერატურაზე ნაკლები!");
    if (tEvap >= tempInternal) warnings.push("⚠️ აორთქლების ტემპერატურა უნდა იყოს 5-8°C დაბალი!");
    if (results.volume > 100) warnings.push("ℹ️ დიდი მოცულობისთვის შეიძლება საჭირო გახდეს რამდენიმე აგრეგატი.");
    if (productLoad / results.volume > 200) warnings.push("⚠️ პროდუქტის დატვირთვა ძალიან მაღალია!");
    return warnings;
  };

  const warnings = getWarnings();

  const downloadReport = () => {
    const res = results;
    const report = `ᲡᲐᲛᲐᲪᲘᲕᲠᲝ ᲡᲘᲡᲢᲔᲛᲘᲡ ᲒᲐᲗᲕᲚᲘᲡ ᲐᲜᲒᲐᲠᲘᲨᲘ\n\nმოცულობა: ${res.volume.toFixed(1)} მ³\nსაჭირო სიმძლავრე: ${res.requiredCapacity.toFixed(2)} kW\n\nკომპრესორი: ${res.selectedCompressor ? `BITZER ${res.selectedCompressor.model} - $${res.selectedCompressor.price}` : 'ვერ მოიძებნა'}\nგამაორთქლებელი: ${res.selectedEvaporator ? `${res.selectedEvaporator.model} - $${res.selectedEvaporator.price}` : 'ვერ მოიძებნა'}\n\nSTOCK LTD © 2026`;
    const blob = new Blob([report], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report_${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{minHeight:'100vh',background:'linear-gradient(135deg, #e3f2fd 0%, #b3e5fc 100%)',padding:'1rem'}}>
      <div style={{maxWidth:'1400px',margin:'0 auto'}}>
        <div style={{background:'white',borderRadius:'12px',boxShadow:'0 4px 6px rgba(0,0,0,0.1)',padding:'1.5rem',marginBottom:'1.5rem'}}>
          <div style={{display:'flex',alignItems:'center',gap:'12px'}}>
            <Thermometer size={40} color="#1976d2" />
            <div>
              <h1 style={{fontSize:'1.875rem',fontWeight:'bold',color:'#1a1a1a',margin:0}}>სამაცივრო აგრეგატის შერჩევა</h1>
              <p style={{color:'#666',margin:0}}>STOCK LTD - პროფესიონალური კალკულატორი</p>
            </div>
          </div>
        </div>

        <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(300px, 1fr))',gap:'1.5rem'}}>
          <div style={{display:'flex',flexDirection:'column',gap:'1rem'}}>
            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.125rem',marginBottom:'1rem',display:'flex',alignItems:'center',gap:'8px'}}>
                <Package size={20} color="#1976d2" />კამერის ზომები
              </h3>
              <div style={{display:'flex',flexDirection:'column',gap:'12px'}}>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>სიგრძე (მ)</label><input type="number" value={length} onChange={e=>setLength(parseFloat(e.target.value)||1)} min="1" step="0.1" style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>სიგანე (მ)</label><input type="number" value={width} onChange={e=>setWidth(parseFloat(e.target.value)||1)} min="1" step="0.1" style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>სიმაღლე (მ)</label><input type="number" value={height} onChange={e=>setHeight(parseFloat(e.target.value)||1)} min="1" step="0.1" style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>იზოლაცია (მმ)</label><select value={insulation} onChange={e=>setInsulation(parseInt(e.target.value))} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}}><option value="60">60</option><option value="80">80</option><option value="100">100 (სტანდარტული)</option><option value="120">120</option><option value="150">150</option><option value="200">200</option></select></div>
                <div style={{fontSize:'0.875rem',color:'#666',background:'#e3f2fd',padding:'8px',borderRadius:'6px'}}>მოცულობა: {results.volume.toFixed(1)} მ³</div>
              </div>
            </div>

            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.125rem',marginBottom:'1rem',display:'flex',alignItems:'center',gap:'8px'}}>
                <Thermometer size={20} color="#d32f2f" />ტემპერატურები
              </h3>
              <div style={{display:'flex',flexDirection:'column',gap:'12px'}}>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>გარე (°C)</label><input type="number" value={tempAmbient} onChange={e=>setTempAmbient(parseFloat(e.target.value)||0)} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>კამერა (°C)</label><input type="number" value={tempInternal} onChange={e=>setTempInternal(parseFloat(e.target.value)||0)} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>აორთქლება (°C)</label><select value={tEvap} onChange={e=>setTEvap(parseInt(e.target.value))} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}}><option value="-5">-5</option><option value="-8">-8</option><option value="-10">-10</option><option value="-25">-25</option><option value="-30">-30</option></select></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>კონდენსაცია (°C)</label><select value={tCond} onChange={e=>setTCond(parseInt(e.target.value))} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}}><option value="35">35</option><option value="40">40</option><option value="45">45</option><option value="50">50</option></select></div>
              </div>
            </div>

            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.125rem',marginBottom:'1rem',display:'flex',alignItems:'center',gap:'8px'}}>
                <Package size={20} color="#388e3c" />პროდუქტი
              </h3>
              <div style={{display:'flex',flexDirection:'column',gap:'12px'}}>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>ტიპი</label><select value={productType} onChange={e=>setProductType(e.target.value)} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}}>{Object.entries(productData).map(([k,v])=><option key={k} value={k}>{v.name}</option>)}</select></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>ბრუნვა (კგ/დღე)</label><input type="number" value={productLoad} onChange={e=>setProductLoad(parseFloat(e.target.value)||0)} min="0" style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>შემომავალი (°C)</label><input type="number" value={productTemp} onChange={e=>setProductTemp(parseFloat(e.target.value)||0)} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}} /></div>
              </div>
            </div>

            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.125rem',marginBottom:'1rem',display:'flex',alignItems:'center',gap:'8px'}}>
                <Settings size={20} color="#666" />დამატებითი
              </h3>
              <div style={{display:'flex',flexDirection:'column',gap:'12px'}}>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>მუშაობა (სთ/დღე): {runHours}</label><input type="range" value={runHours} onChange={e=>setRunHours(parseInt(e.target.value))} min="12" max="24" style={{width:'100%'}} /></div>
                <div><label style={{display:'block',fontSize:'0.875rem',fontWeight:'500',marginBottom:'4px'}}>ფრეონი</label><select value={refrigerant} onChange={e=>setRefrigerant(e.target.value)} style={{width:'100%',padding:'8px 12px',border:'1px solid #ddd',borderRadius:'8px',fontSize:'1rem'}}><option value="R404A">R404A</option><option value="R449A">R449A</option></select></div>
              </div>
            </div>
          </div>

          <div style={{display:'flex',flexDirection:'column',gap:'1rem',gridColumn:'span 2'}}>
            {warnings.length>0&&<div style={{background:'#fff3cd',border:'1px solid #ffc107',borderLeft:'4px solid #ffc107',borderRadius:'8px',padding:'1rem'}}><div style={{display:'flex',gap:'8px'}}><AlertCircle size={20} color="#856404" /><div><h4 style={{fontWeight:'bold',color:'#856404',margin:'0 0 8px 0'}}>გაფრთხილებები:</h4><ul style={{margin:0,paddingLeft:'20px'}}>{warnings.map((w,i)=><li key={i} style={{fontSize:'0.875rem',color:'#856404'}}>{w}</li>)}</ul></div></div></div>}

            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1.5rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.25rem',marginBottom:'1rem',display:'flex',alignItems:'center',gap:'8px'}}>
                <Calculator size={24} color="#1976d2" />გამოთვლილი დატვირთვა
              </h3>
              <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(200px, 1fr))',gap:'1rem',marginBottom:'1rem'}}>
                <div style={{background:'#e3f2fd',padding:'1rem',borderRadius:'8px'}}><div style={{fontSize:'0.875rem',color:'#666'}}>საჭირო სიმძლავრე</div><div style={{fontSize:'1.5rem',fontWeight:'bold',color:'#1976d2'}}>{results.requiredCapacity.toFixed(2)} kW</div></div>
                <div style={{background:'#e8f5e9',padding:'1rem',borderRadius:'8px'}}><div style={{fontSize:'0.875rem',color:'#666'}}>Safety Factor</div><div style={{fontSize:'1.5rem',fontWeight:'bold',color:'#388e3c'}}>+{((results.safetyFactor-1)*100).toFixed(0)}%</div></div>
              </div>
              <button onClick={()=>setShowDetails(!showDetails)} style={{color:'#1976d2',fontSize:'0.875rem',fontWeight:'500',background:'none',border:'none',cursor:'pointer',display:'flex',alignItems:'center',gap:'4px'}}><Info size={16} />{showDetails?'დამალვა':'დეტალური ანგარიში'}</button>
              {showDetails&&<div style={{marginTop:'1rem',fontSize:'0.875rem',borderTop:'1px solid #ddd',paddingTop:'1rem'}}><div style={{display:'flex',justifyContent:'space-between',marginBottom:'8px'}}><span style={{color:'#666'}}>Q1 (კედლები):</span><span style={{fontWeight:'600'}}>{results.qTransmission.toFixed(2)} kW</span></div><div style={{display:'flex',justifyContent:'space-between',marginBottom:'8px'}}><span style={{color:'#666'}}>Q2 (პროდუქტი):</span><span style={{fontWeight:'600'}}>{results.qProduct.toFixed(2)} kW</span></div><div style={{display:'flex',justifyContent:'space-between'}}><span style={{color:'#666'}}>Q3 (დამატებითი):</span><span style={{fontWeight:'600'}}>{results.qAdditional.toFixed(2)} kW</span></div></div>}
            </div>

            <div style={{background:'white',borderRadius:'12px',boxShadow:'0 2px 4px rgba(0,0,0,0.1)',padding:'1.5rem'}}>
              <h3 style={{fontWeight:'bold',fontSize:'1.25rem',marginBottom:'1rem'}}>რეკომენდებული აღჭურვილობა</h3>
              {results.selectedCompressor?<div><div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(250px, 1fr))',gap:'1rem',marginBottom:'1rem'}}>
                <div style={{background:'#d4edda',border:'2px solid #28a745',borderRadius:'8px',padding:'1rem'}}><div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'12px'}}><CheckCircle size={20} color="#155724" /><h4 style={{fontWeight:'bold',fontSize:'1.125rem',margin:0}}>BITZER {results.selectedCompressor.model}</h4></div><div style={{fontSize:'0.875rem'}}><div style={{display:'flex',justifyContent:'space-between',marginBottom:'4px'}}><span style={{color:'#666'}}>სიმძლავრე:</span><span style={{fontWeight:'600'}}>{results.selectedCompressor[results.mode]} kW</span></div><div style={{display:'flex',justifyContent:'space-between',marginBottom:'4px'}}><span style={{color:'#666'}}>EER:</span><span style={{fontWeight:'600'}}>{(results.selectedCompressor[results.mode]/results.selectedCompressor.power).toFixed(1)}</span></div><div style={{display:'flex',justifyContent:'space-between',borderTop:'1px solid #c3e6cb',paddingTop:'8px',marginTop:'8px'}}><span style={{fontWeight:'bold'}}>ფასი:</span><span style={{fontWeight:'bold',color:'#28a745'}}>${results.selectedCompressor.price}</span></div></div></div>
                {results.selectedEvaporator&&<div style={{background:'#cce5ff',border:'2px solid #004085',borderRadius:'8px',padding:'1rem'}}><div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'12px'}}><CheckCircle size={20} color="#004085" /><h4 style={{fontWeight:'bold',fontSize:'1.125rem',margin:0}}>{results.selectedEvaporator.model}</h4></div><div style={{fontSize:'0.875rem'}}><div style={{display:'flex',justifyContent:'space-between',marginBottom:'4px'}}><span style={{color:'#666'}}>სიმძლავრე:</span><span style={{fontWeight:'600'}}>{results.selectedEvaporator.capacity} kW</span></div><div style={{display:'flex',justifyContent:'space-between',borderTop:'1px solid #b8daff',paddingTop:'8px',marginTop:'8px'}}><span style={{fontWeight:'bold'}}>ფასი:</span><span style={{fontWeight:'bold',color:'#004085'}}>${results.selectedEvaporator.price}</span></div></div></div>}
              </div><div style={{background:'#f5f5f5',borderRadius:'8px',padding:'1rem',marginBottom:'1rem'}}><div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}><span style={{fontSize:'1.125rem',fontWeight:'bold'}}>სულ:</span><span style={{fontSize:'1.5rem',fontWeight:'bold',color:'#1976d2'}}>${results.selectedCompressor.price+(results.selectedEvaporator?.price||0)}</span></div><p style={{fontSize:'0.75rem',color:'#666',margin:'8px 0 0 0'}}>* ფასი არ შეიცავს: კონდენსატორს, მილებს, ავტომატიკას, მონტაჟს</p></div><div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'12px'}}><button onClick={downloadReport} style={{flex:1,background:'#1976d2',color:'white',padding:'12px',borderRadius:'8px',fontWeight:'600',border:'none',cursor:'pointer',display:'flex',alignItems:'center',justifyContent:'center',gap:'8px'}}><Download size={20} />ანგარიშის ჩამოტვირთვა</button><button onClick={()=>alert('შეკვეთა გაგზავნილია მენეჯერთან! 📧')} style={{flex:1,background:'#28a745',color:'white',padding:'12px',borderRadius:'8px',fontWeight:'600',border:'none',cursor:'pointer'}}>შეკვეთის გაფორმება</button></div></div>:<div style={{background:'#f8d7da',border:'2px solid #dc3545',borderRadius:'8px',padding:'1.5rem',textAlign:'center'}}><AlertCircle size={48} color="#721c24" style={{margin:'0 auto 12px'}} /><h4 style={{fontWeight:'bold',fontSize:'1.125rem',color:'#721c24',margin:'0 0 8px 0'}}>შესაბამისი მოდელი ვერ მოიძებნა</h4><p style={{color:'#721c24',margin:'0 0 8px 0'}}>საჭირო სიმძლავრე ({results.requiredCapacity.toFixed(2)} kW) აჭარბებს დიაპაზონს.</p><p style={{fontSize:'0.875rem',color:'#666',margin:0}}>რეკომენდაცია: შეამცირეთ პარამეტრები</p></div>}
            </div>

            <div style={{background:'linear-gradient(135deg, #e3f2fd 0%, #b3e5fc 100%)',borderRadius:'8px',border:'1px solid #81d4fa',padding:'1rem'}}><h4 style={{fontWeight:'bold',fontSize:'1rem',marginBottom:'12px'}}>ℹ️ მნიშვნელოვანი ინფორმაცია</h4><div style={{fontSize:'0.875rem',color:'#333',lineHeight:'1.6'}}><p><strong>აორთქლება (Te):</strong> უნდა იყოს კამერაზე 5-8°C დაბალი</p><p><strong>კონდენსაცია (Tc):</strong> ზაფხულში 45-50°C, ზამთარში 35-40°C</p><p><strong>Safety Factor:</strong> 15% (საშუალო), 25% (Te&lt;-15°C), 30% (Te&lt;-25°C)</p><p style={{marginBottom:0}}><strong>გათვლა მოიცავს:</strong> კედლების გამტარობას, პროდუქტის გაცივებას, განათებას, ადამიანებს, კარის გახსნებს</p></div></div>
          </div>
        </div>

        <div style={{marginTop:'1.5rem',textAlign:'center',fontSize:'0.875rem',color:'#666',background:'white',borderRadius:'8px',padding:'1rem'}}><p style={{margin:'0 0 8px 0'}}><strong>შენიშვნა:</strong> გათვლები ეფუძნება სტანდარტულ პირობებს და R404A/R449A მონაცემებს. ზუსტი პროექტირებისთვის საჭიროა ობიექტზე დათვალიერება.</p><p style={{margin:0,fontSize:'0.75rem'}}>STOCK LTD © 2026 | ტექნიკური მხარდაჭერა: +995 XXX XXX XXX</p></div>
      </div>
    </div>
  );
};

export default RefrigerationCalculator;
