export type NavigationBarConfig = {
  items: {
    name: string
    label: string
    icon: string
    activeIcon: string
  }[]
}

export type IconSize = 'small' | 'normal' | 'large'

export type IconItemConfig = {
  size: {
    [size in IconSize]: string
  }
}

// TODO: Handle undefined opional fields: birthDate, entryDate, yard, ...
export type Animal = {
  id: number
  name: string
  personality: string
  description: string
  sex: 'male' | 'female'
  birthDate: Date
  entryDate: Date
  yard: Yard
  isAnimalCompatible: boolean
  isCastrated: boolean
  image?: string
}

export type Yard = {
  id: number
  name: string
}

export type TextFilter = {
  type: 'text'
  item: string
}

export type ContentFilter = {
  type: 'content'
  item: any[]
}

export type Filters = Record<string, TextFilter | ContentFilter>

export type User = {
  name: string
  surnames: string
  email: string
  isVeteran: boolean
  avatar?: string
}

export type AnimalFilters = {
  name: string
  yards: { [yard: string]: boolean }
  sex: { [sex: string]: boolean }
  age: {
    min: number
    max: number
  }
  castration: { [castration: string]: boolean }
  compatible: { [compatible: string]: boolean }
}

export type Notification = {
  id: string
  text: string
  icon?: string
  cardStyle?: string
  textStyle?: string
  iconStyle?: string
}
