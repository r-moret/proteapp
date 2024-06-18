import type { User, Animal, Treatment, MedicalAppointment } from '@/types'
export const fakeUser: User = {
  name: 'Alberto',
  surnames: 'Martínez',
  email: 'amartinez@gmail.com',
  isVeteran: true
}

export const fakeYards = ['Patio 1', 'Patio 2', 'Patio 3', 'Patio inmuno', 'Patio 4']

export const fakeAppointments: MedicalAppointment[] = [
  { id: '1', date: new Date('2011-10-10T15:00:00'), reason: 'vacuna' },
  { id: '2', date: new Date('2020-12-10T16:00:00'), reason: 'cura' },
  { id: '3', date: new Date('2024-10-10T22:00:00'), reason: 'castracion' }
]

export const fakeTreatments: Treatment[] = [
  {
    id: '1',
    name: 'Paracetamol',
    zone: 'Cabeza',
    freq: 3,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  },
  {
    id: '2',
    name: 'Ibuprofeno',
    zone: 'Cuello',
    freq: 5,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  },
  {
    id: '3',
    name: 'Aspirina',
    zone: 'Pata',
    freq: 5,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  },
  {
    id: '4',
    name: 'Betadine',
    zone: 'Cabeza',
    freq: 7,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  },
  {
    id: '5',
    name: 'Pipeta',
    zone: 'Escapulas',
    freq: 10,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  },
  {
    id: '6',
    name: 'Clhorexidina',
    zone: 'Pata derecha',
    freq: 25,
    animalId: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e'
  }
]

export const fakeAnimals: Animal[] = [
  {
    id: 'f6b681ac-2b60-4b7d-a017-f490e8a8c10e',
    image: 'https://cdn2.thecatapi.com/images/9vh.jpg',
    name: 'Carolina',
    description:
      'Carolina es una hermosa gata con un pelaje suave y lujoso. Disfruta tomando el sol y acurrucándose con sus compañeros humanos. A pesar de su apariencia regia, Carolina es increíblemente amigable y le encanta conocer gente nueva y otros animales.',
    personality: 'Amistosa y curiosa',
    sex: 'female',
    birthDate: new Date('2011-10-10'),
    entryDate: new Date('2022-10-09'),
    isCastrated: true,
    isAnimalCompatible: true,
    yard: 'Patio 1',
    hasTreatment: true,
    treatmentList: ['2', '3', '1'],
    appointmentList: ['1', '2', '3']
  },
  {
    id: '51ccd7f1-65db-4dcd-86b3-2387b95d6900',
    image: 'https://cdn2.thecatapi.com/images/def.jpg',
    name: 'Luna',
    description:
      'Luna es una gatita tímida y cariñosa. Prefiere pasar su tiempo acurrucada en una cama suave, pero una vez que se siente cómoda, le encanta recibir caricias y atención de sus seres queridos.',
    personality: 'Tímida y cariñosa',
    sex: 'female',
    birthDate: new Date('2018-02-28'),
    entryDate: new Date('2023-01-10'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio 1',
    hasTreatment: true,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: '400bedd5-d77f-41af-86b7-82ee6d6fa8bf',
    image: 'https://cdn2.thecatapi.com/images/abc.jpg',
    name: 'Simón',
    description:
      'Simón es un gato juguetón y enérgico. Le encanta correr por toda la casa persiguiendo juguetes y explorando cada rincón. Siempre está listo para una sesión de juego con su familia humana.',
    personality: 'Juguetón y enérgico',
    sex: 'male',
    birthDate: new Date('2019-05-15'),
    entryDate: new Date('2022-12-20'),
    isCastrated: false,
    isAnimalCompatible: true,
    yard: 'Patio 2',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: 'b7051f60-bff7-4cb9-b2a1-f559fd1abf6b',
    image: 'https://cdn2.thecatapi.com/images/27r.jpg',
    name: 'Tiger',
    description:
      'Tiger es un gato aventurero y valiente. Le encanta explorar los alrededores y nunca dice que no a una nueva aventura. Su coraje y espíritu intrépido lo hacen destacar entre los demás.',
    personality: 'Aventurero y valiente',
    sex: 'male',
    birthDate: new Date('2020-07-03'),
    entryDate: new Date('2023-03-22'),
    isCastrated: false,
    isAnimalCompatible: false,
    yard: 'Patio inmuno',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: '52f35395-0206-44c8-a456-44f0728b2b1c',
    image: '',
    name: 'Mia',
    description:
      'Mia es una gata tranquila y elegante. Disfruta pasar horas observando su entorno desde la ventana y relajarse en lugares cálidos y cómodos. Su gracia y calma son dignas de admiración.',
    personality: 'Tranquila y elegante',
    sex: 'female',
    birthDate: new Date('2017-11-20'),
    entryDate: new Date('2023-06-18'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio 4',
    hasTreatment: true,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: 'f61f8574-ceaa-41a4-a3c3-d3d1ee9b175e',
    image: 'https://cdn2.thecatapi.com/images/afm.jpg',
    name: 'Max',
    description:
      'Max es un gato inteligente y leal. Siempre está atento a las necesidades de su familia humana y es rápido para ofrecer consuelo cuando lo necesitan. Su lealtad no tiene límites.',
    personality: 'Inteligente y leal',
    sex: 'male',
    birthDate: new Date('2016-04-12'),
    entryDate: new Date('2023-09-05'),
    isCastrated: false,
    isAnimalCompatible: true,
    yard: 'Patio 1',
    hasTreatment: true,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: 'a2e167a6-f666-474c-b6c4-db7fb50417d8',
    image: 'https://cdn2.thecatapi.com/images/pqr.jpg',
    name: 'Lola',
    description:
      'Lola es una gatita traviesa y juguetona. Siempre está buscando nuevas formas de divertirse y mantener entretenida a su familia humana. Su energía contagiosa ilumina cualquier habitación.',
    personality: 'Traviesa y juguetona',
    sex: 'female',
    birthDate: new Date('2021-01-08'),
    entryDate: new Date('2023-11-11'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio 2',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: 'cc0876bb-c981-4ff6-89f3-4e404b06b256',
    image: 'https://cdn2.thecatapi.com/images/58l.jpg',
    name: 'Tomás',
    description:
      'Tomás es un gato curioso y sociable. Siempre está interesado en lo que sucede a su alrededor y no duda en acercarse a nuevos amigos, tanto humanos como felinos. Su naturaleza amistosa lo convierte en el alma de la fiesta.',
    personality: 'Curioso y sociable',
    sex: 'male',
    birthDate: new Date('2015-09-25'),
    entryDate: new Date('2024-02-19'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio inmuno',
    hasTreatment: true,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: '736b744f-b4f9-47ea-aa05-e4869f381395',
    image: 'https://cdn2.thecatapi.com/images/MTg0NDAwNw.jpg',
    name: 'Molly',
    description:
      'Molly es una gatita dulce y cariñosa. Le encanta pasar tiempo acurrucada en el regazo de sus seres queridos y recibir mimos y caricias. Su afecto incondicional es una fuente constante de alegría.',
    personality: 'Dulce y cariñosa',
    sex: 'female',
    birthDate: new Date('2014-12-03'),
    entryDate: new Date('2024-04-05'),
    isCastrated: true,
    isAnimalCompatible: true,
    yard: 'Patio 3',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: '40fe9f90-0987-4bf1-9b3e-3f012286bc54',
    image: 'https://cdn2.thecatapi.com/images/MTg4ODgzNw.jpg',
    name: 'Leo',
    description:
      'Leo es un gato independiente y audaz. Disfruta explorando por su cuenta y no se intimida fácilmente ante lo desconocido. Su espíritu libre lo hace admirado por todos.',
    personality: 'Independiente y audaz',
    sex: 'male',
    birthDate: new Date('2013-06-17'),
    entryDate: new Date('2024-05-10'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio 4',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: 'bd92bf83-af55-4361-8d39-8aee67ec2ac6',
    image: 'https://cdn2.thecatapi.com/images/417.jp',
    name: 'Lulu',
    description:
      'Lola es una gatita enérgica y cariñosa. Siempre está lista para jugar y correr por la casa, pero también disfruta de largas siestas en el sol. Su personalidad versátil la hace amada por todos.',
    personality: 'Enérgica y cariñosa',
    sex: 'female',
    birthDate: new Date('2019-08-22'),
    entryDate: new Date('2024-06-15'),
    isCastrated: false,
    isAnimalCompatible: false,
    yard: 'Patio 1',
    hasTreatment: true,
    treatmentList: [],
    appointmentList: []
  },
  {
    id: '021392fe-d8bf-41fb-bc05-a0d6e476a8f0',
    image: 'https://cdn2.thecatapi.com/images/301.jpg',
    name: 'Simba',
    description:
      'Simba es un gato noble y protector. Siempre está vigilando su territorio y asegurándose de que su familia esté a salvo. Su coraje y devoción son incomparables.',
    personality: 'Noble y protector',
    sex: 'male',
    birthDate: new Date('2017-03-30'),
    entryDate: new Date('2024-07-20'),
    isCastrated: true,
    isAnimalCompatible: false,
    yard: 'Patio inmuno',
    hasTreatment: false,
    treatmentList: [],
    appointmentList: []
  }
]
