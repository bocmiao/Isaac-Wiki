import { int, type DonationProgress } from './storage'
/** A blank field does not assert that a character has donated zero coins. */
export function calibrateDonations(current:DonationProgress,who:string,greed:unknown,normal:unknown,personal:unknown):DonationProgress|null {
 if(!int(greed,1000)||!int(normal,999)||(personal!==''&&!int(personal,1000000)))return null
 const characters={...current.characters}
 if(personal!=='')characters[who]=personal as number
 return {...current,greed:greed as number,normal:normal as number,characters}
}
export function confirmedShopLevel(progress:DonationProgress){
 return [151,152,153,154].reduce((level,id,index)=>progress.normalUnlocked?.includes(id)?index+1:level,0)
}
